# Changelog

## [Unreleased](https://github.com/EMMC-ASBL/otelib/tree/HEAD)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/v0.5.0.dev1...HEAD)

## DX and dependency updates

Remove the use of an extra permanent dependencies branch to create aggregated dependency update PRs.
Instead use dependabot's groups feature.

Update the dependencies and dev tools.

**Implemented enhancements:**

- Optimize CI/CD by using dependabot's groups [\#238](https://github.com/EMMC-ASBL/otelib/issues/238)
- Use Trusted Publisher from PyPI [\#237](https://github.com/EMMC-ASBL/otelib/issues/237)

## [v0.5.0.dev1](https://github.com/EMMC-ASBL/otelib/tree/v0.5.0.dev1) (2024-09-18)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/v0.5.0.dev0...v0.5.0.dev1)

## DX and dependency updates

Remove the use of an extra permanent dependencies branch to create aggregated dependency update PRs.
Instead use dependabot's groups feature.

Update the dependencies and dev tools.

**Merged pull requests:**

- Update CI/CD and use Trusted Publisher from PyPI [\#236](https://github.com/EMMC-ASBL/otelib/pull/236) ([CasperWA](https://github.com/CasperWA))

## [v0.5.0.dev0](https://github.com/EMMC-ASBL/otelib/tree/v0.5.0.dev0) (2024-03-08)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/v0.4.1...v0.5.0.dev0)

**Fixed bugs:**

- Real backend tests failing [\#151](https://github.com/EMMC-ASBL/otelib/issues/151)

**Closed issues:**

- Fix otelib to handle parser [\#178](https://github.com/EMMC-ASBL/otelib/issues/178)

**Merged pull requests:**

- Add create parser function [\#174](https://github.com/EMMC-ASBL/otelib/pull/174) ([Treesarj](https://github.com/Treesarj))
- Update README [\#173](https://github.com/EMMC-ASBL/otelib/pull/173) ([torhaugl](https://github.com/torhaugl))
- Don't use filesamples.com [\#152](https://github.com/EMMC-ASBL/otelib/pull/152) ([CasperWA](https://github.com/CasperWA))

## [v0.4.1](https://github.com/EMMC-ASBL/otelib/tree/v0.4.1) (2023-10-25)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/v0.4.0...v0.4.1)

**Closed issues:**

- Support Python 3.11 [\#120](https://github.com/EMMC-ASBL/otelib/issues/120)

**Merged pull requests:**

- Extend support to Python 3.11 [\#136](https://github.com/EMMC-ASBL/otelib/pull/136) ([CasperWA](https://github.com/CasperWA))

## [v0.4.0](https://github.com/EMMC-ASBL/otelib/tree/v0.4.0) (2023-10-19)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/v0.3.2...v0.4.0)

**Implemented enhancements:**

- Use ruff [\#130](https://github.com/EMMC-ASBL/otelib/issues/130)
- Migrate to pydantic v2 [\#129](https://github.com/EMMC-ASBL/otelib/issues/129)

**Fixed bugs:**

- Fix test issue [\#132](https://github.com/EMMC-ASBL/otelib/pull/132) ([CasperWA](https://github.com/CasperWA))

**Closed issues:**

- Use latest SINTEF/ci-cd [\#137](https://github.com/EMMC-ASBL/otelib/issues/137)
- Revert update of codecov-action from v4 to v3 [\#127](https://github.com/EMMC-ASBL/otelib/issues/127)
- Update documentation [\#7](https://github.com/EMMC-ASBL/otelib/issues/7)

**Merged pull requests:**

- Update SINTEF/ci-cd usage to v2.5.2 \(was v1\) [\#135](https://github.com/EMMC-ASBL/otelib/pull/135) ([CasperWA](https://github.com/CasperWA))
- Migrate to pydantic v2 [\#133](https://github.com/EMMC-ASBL/otelib/pull/133) ([CasperWA](https://github.com/CasperWA))
- Use ruff [\#131](https://github.com/EMMC-ASBL/otelib/pull/131) ([CasperWA](https://github.com/CasperWA))

## [v0.3.2](https://github.com/EMMC-ASBL/otelib/tree/v0.3.2) (2023-06-20)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/v0.3.1...v0.3.2)

**Closed issues:**

- Fix: input\_pipe  not set correctly when two pipelines are merged [\#110](https://github.com/EMMC-ASBL/otelib/issues/110)

**Merged pull requests:**

- Doi badge [\#115](https://github.com/EMMC-ASBL/otelib/pull/115) ([jesper-friis](https://github.com/jesper-friis))
- Add checks to make sure input\_pipe is set to the first filter [\#111](https://github.com/EMMC-ASBL/otelib/pull/111) ([Treesarj](https://github.com/Treesarj))

## [v0.3.1](https://github.com/EMMC-ASBL/otelib/tree/v0.3.1) (2023-05-24)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/v0.3.0...v0.3.1)

**Merged pull requests:**

- Enh/add auth [\#96](https://github.com/EMMC-ASBL/otelib/pull/96) ([MBueschelberger](https://github.com/MBueschelberger))

## [v0.3.0](https://github.com/EMMC-ASBL/otelib/tree/v0.3.0) (2023-04-19)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/v0.2.0...v0.3.0)

**Implemented enhancements:**

- Use flit instead of setuptools [\#76](https://github.com/EMMC-ASBL/otelib/issues/76)
- Use SINTEF/ci-cd [\#74](https://github.com/EMMC-ASBL/otelib/issues/74)

**Fixed bugs:**

- Update tests to support updated celery strategy [\#101](https://github.com/EMMC-ASBL/otelib/issues/101)

**Closed issues:**

- Improve test startup for backend strategies [\#69](https://github.com/EMMC-ASBL/otelib/issues/69)
- Have all clients inherit from the same base class.  [\#68](https://github.com/EMMC-ASBL/otelib/issues/68)
- Improved caching for python backend  [\#66](https://github.com/EMMC-ASBL/otelib/issues/66)

**Merged pull requests:**

- Celery updates [\#103](https://github.com/EMMC-ASBL/otelib/pull/103) ([CasperWA](https://github.com/CasperWA))
- Renamed argument of Pipe.get\(\) to `session_id` to reduce confusion [\#91](https://github.com/EMMC-ASBL/otelib/pull/91) ([jesper-friis](https://github.com/jesper-friis))
- Update CI/CD & use `flit` build system [\#77](https://github.com/EMMC-ASBL/otelib/pull/77) ([CasperWA](https://github.com/CasperWA))

## [v0.2.0](https://github.com/EMMC-ASBL/otelib/tree/v0.2.0) (2022-11-09)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/v0.1.0...v0.2.0)

**Implemented enhancements:**

- Implement direct Python API usage [\#52](https://github.com/EMMC-ASBL/otelib/issues/52)

**Fixed bugs:**

- CI docker service connection issues [\#40](https://github.com/EMMC-ASBL/otelib/issues/40)

**Closed issues:**

- Update pylint options [\#79](https://github.com/EMMC-ASBL/otelib/issues/79)
- I think this part, which is repeated over and over can be simplified, but I'll have to think more about it. Perhaps this could be part of a separate issue and PR? :\) [\#65](https://github.com/EMMC-ASBL/otelib/issues/65)

**Merged pull requests:**

- Use recursive option for pylint-tests in CI [\#80](https://github.com/EMMC-ASBL/otelib/pull/80) ([CasperWA](https://github.com/CasperWA))
- Split client backends - add Python backend [\#60](https://github.com/EMMC-ASBL/otelib/pull/60) ([daniel-sintef](https://github.com/daniel-sintef))
- Use docker instead of docker-compose for CI [\#58](https://github.com/EMMC-ASBL/otelib/pull/58) ([CasperWA](https://github.com/CasperWA))
- Added PR template with checklist for reviewers. [\#37](https://github.com/EMMC-ASBL/otelib/pull/37) ([francescalb](https://github.com/francescalb))
- Update README.md [\#34](https://github.com/EMMC-ASBL/otelib/pull/34) ([quaat](https://github.com/quaat))

## [v0.1.0](https://github.com/EMMC-ASBL/otelib/tree/v0.1.0) (2022-03-15)

[Full Changelog](https://github.com/EMMC-ASBL/otelib/compare/8ff7c18ed6a0eeac9129d57fe0f201f645cce82c...v0.1.0)

**Implemented enhancements:**

- Add Function strategy [\#28](https://github.com/EMMC-ASBL/otelib/issues/28)
- Rename test file [\#18](https://github.com/EMMC-ASBL/otelib/issues/18)
- Release on PyPI [\#12](https://github.com/EMMC-ASBL/otelib/issues/12)
- Setup development tools and CI [\#9](https://github.com/EMMC-ASBL/otelib/issues/9)
- Add more tests [\#3](https://github.com/EMMC-ASBL/otelib/issues/3)

**Fixed bugs:**

- Fix issue with SQL filter [\#25](https://github.com/EMMC-ASBL/otelib/issues/25)
- Update to oteapi-core v0.1 [\#16](https://github.com/EMMC-ASBL/otelib/issues/16)
- Fix issue with GH GraphQL type in auto-merge CI workflow [\#13](https://github.com/EMMC-ASBL/otelib/issues/13)

**Closed issues:**

- Add dependabot with CI/CD workflows [\#14](https://github.com/EMMC-ASBL/otelib/issues/14)
- rename name in setup.py [\#10](https://github.com/EMMC-ASBL/otelib/issues/10)
- Make otelib pip installable [\#6](https://github.com/EMMC-ASBL/otelib/issues/6)
- Set up testing framework [\#5](https://github.com/EMMC-ASBL/otelib/issues/5)
- Rename OntoTransServer [\#4](https://github.com/EMMC-ASBL/otelib/issues/4)
- Clean up repository and use oteapi-core and oteapi-services [\#1](https://github.com/EMMC-ASBL/otelib/issues/1)

**Merged pull requests:**

- Add Function strategy [\#30](https://github.com/EMMC-ASBL/otelib/pull/30) ([CasperWA](https://github.com/CasperWA))
- Add more tests [\#27](https://github.com/EMMC-ASBL/otelib/pull/27) ([CasperWA](https://github.com/CasperWA))
- Fix testing for filters [\#26](https://github.com/EMMC-ASBL/otelib/pull/26) ([CasperWA](https://github.com/CasperWA))
- Correct typo in readme [\#23](https://github.com/EMMC-ASBL/otelib/pull/23) ([jesper-friis](https://github.com/jesper-friis))
- Fix tests and implement extra debugging messages [\#17](https://github.com/EMMC-ASBL/otelib/pull/17) ([CasperWA](https://github.com/CasperWA))
- Add dependabot for dependency updates [\#15](https://github.com/EMMC-ASBL/otelib/pull/15) ([CasperWA](https://github.com/CasperWA))
- Add CI/CD and pre-commit [\#11](https://github.com/EMMC-ASBL/otelib/pull/11) ([CasperWA](https://github.com/CasperWA))
- Rename ontotranserver to server [\#8](https://github.com/EMMC-ASBL/otelib/pull/8) ([Treesarj](https://github.com/Treesarj))
- Cleaned up  [\#2](https://github.com/EMMC-ASBL/otelib/pull/2) ([jesper-friis](https://github.com/jesper-friis))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
