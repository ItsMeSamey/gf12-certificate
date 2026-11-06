"""Check a fixed-field bilinear multiplication certificate using only stdlib.

Certificates are JSON data. No certificate value is imported or executed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

DEGREE = 12
MODULUS = 0x1053
TERM_COUNT = 42
MAX_INPUT_BYTES = 16 * 1024
FIELD = {"degree": DEGREE, "modulus": MODULUS,
         "basis": "polynomial", "bit_order": "little-endian"}


class CertificateError(ValueError):
    def __init__(self, code, location, message):
        super().__init__(message)
        self.code = code
        self.location = location


def fail(code, location, message):
    raise CertificateError(code, location, message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail("duplicate_key", "$", "Duplicate JSON object key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    fail("json_number", "$", "Non-finite JSON number is not permitted")


def exact_keys(value, expected, location):
    if type(value) is not dict:
        fail("object_type", location, "Expected a JSON object")
    if set(value) != set(expected):
        fail("object_keys", location, "Expected exactly these keys: " + ", ".join(sorted(expected)))


def parse_certificate(raw):
    if type(raw) is not bytes:
        fail("input_type", "$", "Expected UTF-8 bytes")
    if len(raw) > MAX_INPUT_BYTES:
        fail("input_size", "$", "Fixed 42-term certificate exceeds the 16384-byte input limit")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                           parse_constant=reject_constant)
    except CertificateError:
        raise
    except (UnicodeError, ValueError, RecursionError) as error:
        fail("json_syntax", "$", "Invalid UTF-8 JSON: " + type(error).__name__)
    exact_keys(value, {"schema_version", "field", "terms"}, "$")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        fail("schema_version", "$.schema_version", "Only integer schema version 1 is supported")
    field = value["field"]
    exact_keys(field, FIELD, "$.field")
    for key, expected in FIELD.items():
        if type(field[key]) is not type(expected) or field[key] != expected:
            fail("field_contract", "$.field." + key, "Unsupported fixed-field declaration")
    terms = value["terms"]
    if type(terms) is not list or len(terms) != TERM_COUNT:
        fail("term_count", "$.terms", "Expected exactly 42 term triples")
    for index, term in enumerate(terms):
        location = "$.terms[" + str(index) + "]"
        if type(term) is not list or len(term) != 3:
            fail("triple_shape", location, "Each term must be a three-element JSON array")
        for axis, mask in enumerate(term):
            if type(mask) is not int or not 0 <= mask < (1 << DEGREE):
                fail("mask_type_range", location + "[" + str(axis) + "]",
                     "Masks must be integers from 0 to 4095; booleans and floats are not integers here")
    return value


def reference_product(left, right):
    """Carryless coefficient convolution, then long division in GF(2)[X]."""
    polynomial = 0
    for i in range(DEGREE):
        if (left >> i) & 1:
            for j in range(DEGREE):
                if (right >> j) & 1:
                    polynomial ^= 1 << (i + j)
    for degree in range(2 * DEGREE - 2, DEGREE - 1, -1):
        if (polynomial >> degree) & 1:
            polynomial ^= MODULUS << (degree - DEGREE)
    return polynomial


def tensor_product(terms, left, right):
    result = 0
    for a_mask, b_mask, c_mask in terms:
        if ((a_mask & left).bit_count() & 1) and ((b_mask & right).bit_count() & 1):
            result ^= c_mask
    return result


def check(raw):
    certificate = parse_certificate(raw)
    first = None
    mismatches = 0
    for i in range(DEGREE):
        for j in range(DEGREE):
            left, right = 1 << i, 1 << j
            expected = reference_product(left, right)
            actual = tensor_product(certificate["terms"], left, right)
            if actual != expected:
                mismatches += 1
                if first is None:
                    first = {"left_bit": i, "right_bit": j, "left": left, "right": right,
                             "expected": expected, "actual": actual,
                             "difference": expected ^ actual}
    canonical = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {"status": "semantic_failure" if mismatches else "verified",
            "field": FIELD.copy(), "terms": TERM_COUNT, "basis_pairs_checked": DEGREE * DEGREE,
            "mismatching_basis_pairs": mismatches, "first_witness": first,
            "input_sha256": hashlib.sha256(raw).hexdigest(),
            "canonical_sha256": hashlib.sha256(canonical).hexdigest(),
            "scope": "Classical bilinear multiplication modulo 0x1053 only; no quantum-circuit or cost certification"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", help="UTF-8 JSON certificate file, or - for stdin")
    args = parser.parse_args(argv)
    try:
        if args.certificate == "-":
            if sys.stdin is None:
                raise OSError("Standard input is unavailable")
            raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        else:
            with Path(args.certificate).open("rb") as stream:
                raw = stream.read(MAX_INPUT_BYTES + 1)
        result = check(raw)
        code = 0 if result["status"] == "verified" else 1
    except CertificateError as error:
        result = {"status": "invalid_certificate", "error": {"code": error.code,
                  "location": error.location, "message": str(error)}}
        code = 2
    except OSError as error:
        result = {"status": "input_error", "error": {"code": "file_io", "message": str(error)}}
        code = 2
    result["runtime"] = {"python": sys.version.split()[0], "isolated": bool(sys.flags.isolated),
                         "no_site": bool(sys.flags.no_site), "site_loaded": "site" in sys.modules,
                         "non_stdlib_modules": sorted(name for name in sys.modules
                             if name.split(".")[0] not in sys.stdlib_module_names
                             and name not in {"__main__"})}
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
