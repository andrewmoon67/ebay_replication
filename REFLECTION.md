run_all.sh executes commands sequentially every time it is run, regardless of whether any inputs have changed. 
In contrast, the Makefile explicitly defines the dependency relationships between files in the project. 
This allows Make to rebuild only the outputs whose inputs have changed, making the workflow more efficient. 
The Makefile also documents the structure of the project by clearly showing which scripts produce which outputs 
and how those outputs feed into the final paper.
