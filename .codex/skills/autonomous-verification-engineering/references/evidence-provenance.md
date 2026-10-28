# Content-bound observations

An observation should identify subject, method, actor/tool, time, environment, inputs and result artifact. [SLSA provenance v1.2](https://slsa.dev/spec/v1.2/provenance) is useful for distinguishing how an artifact was produced from whether it satisfies a functional requirement; adopting these design ideas does not claim SLSA compliance.

Hash bytes actually observed. Keep the old record when an input changes; append a new observation after rerunning or reexamining the relevant method. Hash equality supports identity, not authenticity or adequacy of an oracle. Include fixtures, configuration and the acceptance contract as dependencies, not only source code.

For a cache of verdicts, compute freshness from the dependency set. If evidence E covers code A and oracle X, changing unrelated B should not invalidate E; changing X must. Recovery should display stale evidence as historical until the required method has run against current inputs. Never update hashes around an old result to make it look fresh.
