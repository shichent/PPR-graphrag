## Personalized PageRank for GraphRAG
- This repository contains codes to test Personalized PageRank for retrieval step of GraphRAG

## GraphRAG backbone
- We use Tencent's youtu-GraphRAG with some customization and modifications.
- Major change:
    1. Removed schema evolution and switched to async prompting to significantly speed up graph generation (improve from more than 10hrs to about 30 minutes)
    2. Fixed a few bugs in LLM response parsing to eliminate errors and unexpected behaviors in experiment
    3. Created notebooks to study graph topology of LLM generated graph
    4. Implemented an optional Personalized PageRank approach for retrieval step
    
- Instructions to run GraphRAG:
    1. Configure LLM models and keys in .env
    2. Set up configs as a yaml file
    3. Run in CLI: python main.py --datasets [name of dataset] --config [yaml config file] 
