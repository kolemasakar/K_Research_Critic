# Stage131 release candidate wheelhouse — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

Source used: verified git checkout `f122786d0e65b8e7beab9fdaf6ccf360dcd6e44c`. Platform: CPython 3.12, Linux x86_64. Wheelhouse: `/home/krcops/stage131-wheelhouse` (host-local only, **not** part of the Git repository). This records one concrete resolution, not a multi-platform lock or signed software supply-chain attestation.

`pip download -r requirements-stage131-test.txt -d /home/krcops/stage131-wheelhouse` resolved 19 wheels. Their local `sha256sum` values:

```text
2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9  pygments-2.21.0-py3-none-any.whl
33e4fb41ca352810eb4e9838aa0d82d6888a5f8bf682f43e99cce5faa666255c  pypdf-6.21.4-py3-none-any.whl
381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231  referencing-0.37.0-py3-none-any.whl
42269a8a5b3fd54ffa6f3d84b18abed50064717576b4ecf03dc4a55d8aa04fdc  python_dotenv-1.2.4-py3-none-any.whl
481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  typing_extensions-4.16.0-py3-none-any.whl
65b8397ba37ccbce054456aaccddfc91e6e3083c92824df348d96ca832f3f147  typing_inspection-0.4.4-py3-none-any.whl
78cb2c6865a35ab8ff8b75fd122f6033b92a62c82801110e48ddd6c936a45d91  pillow-12.3.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
7dd7b0d8832ba3cb632c306926ded123429211b83641b35dc5c41ad2d34f9bec  pluggy-1.7.0-py3-none-any.whl
872f880de3fc3a5bdc88a11b39c9710c3497a547cfa9320bc3c5e62fbf272e79  pytest-8.4.2-py3-none-any.whl
9121e2c1fdb355232495be3194c8dfe87ccc2d5dee45947b78e68f499790d7a7  iniconfig-2.3.1-py3-none-any.whl
9195d967ec791692a04438115466764fb8b9a27b31f14a760437694f40d6b454  pydantic-2.14.1-py3-none-any.whl
93ba4e9d8210d941c200431a56b2c0400b131865947903937ed3ec5404307d2e  pydantic_core-2.50.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe  jsonschema_specifications-2025.9.1-py3-none-any.whl
addeda51556dac7c1a2f14cda62db8b621cd12afba3091d03a96c72932387eab  rpds_py-2026.9.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
ba1cc08a7ccde2d2ec775841541641e4548226580ab850948cbfda66a1befcdc  pyyaml-6.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309  attrs-26.1.0-py3-none-any.whl
d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce  jsonschema-4.26.0-py3-none-any.whl
d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c  packaging-26.3-py3-none-any.whl
f072f4d804ea359e4eaf198b1af7a8b0943881a87f31bb764f8bf219bb9419e0  annotated_types-0.8.0-py3-none-any.whl
```

Independent second venv created at `/home/krcops/stage131-release-verify-venv`. Installed using `pip install --no-index --find-links=/home/krcops/stage131-wheelhouse -r .../requirements-stage131-test.txt` with no index; `pip check` yielded **No broken requirements found**. Five focused suites: entrypoint, runtime permissions, request schema, private HTTP GET and PDF inventory: **19/19 PASS in 1.72 s**.

**Remaining:** hash-enforcing `pip --require-hashes` lock, per-architecture build, supply-chain source verification, root-owned immutable /opt release, reviewed systemd unit with real SHA and service UID, real owner consent, Sentinel transport restoration and scientific E2E. No service installation or start.
