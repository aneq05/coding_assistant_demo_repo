# Python guidelines

- Target Python 3.12+ and use typed Python.
- Prefer the standard library; justify every new runtime dependency.
- Use simple functions and data structures, explicit readable code, small
  modules, and clear responsibilities over clever abstractions.
- Keep domain logic independent from CLI rendering. Keep future filesystem and
  storage concerns outside domain calculations.
- Use `pathlib` for filesystem paths where appropriate.
- Handle expected invalid input explicitly; do not broadly swallow exceptions.
- Keep deterministic domain calculations easy to unit test.
- Avoid premature service, repository, and dependency-injection abstractions.
