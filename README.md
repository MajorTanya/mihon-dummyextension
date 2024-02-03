# Dummy Extension repository for debugging extension management in Tachiyomi, Mihon, and their forks

This repo contains a singular extension called "Dummy Extension", which does not serve any sort of
content. It explicitly doesn't support any of the operations of the Tachiyomi extensions-lib 1.4 or
newer. The sole purpose of this repo and extension is to aid in debugging aspects like adding
third-party repos, installing/updating/uninstalling extensions, etc., from within Tachiyomi/Mihon or
a fork without having to find an actual repository and depending on sporadic/nonexistent updates for
live extensions.

Again, **THIS EXTENSION DOES NOT SERVE ANY CONTENT WHATSOEVER.**

# Updates

Currently, the DummyExtension is manually updated about _once per week_. In the future, the plan is
to automate the release of new versions and increase the frequency to a few times per week, possibly
daily.

# Usage

Repository index.min.json:

```text
https://raw.githubusercontent.com/MajorTanya/mihon-dummyextension/repo/index.min.json
```

1. Add the repository link from above to your Mihon or Tachiyomi/Mihon-based fork as a third-party
   repository.

2. Install/update the "Dummy Extension" from the list as required for your debugging.

## License

    Copyright 2024 MajorTanya

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
