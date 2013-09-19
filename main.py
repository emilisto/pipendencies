from .requirements import check_requirements, Requirement

with open('./sample_requirements.txt') as f:
    requirements = check_requirements(f.readlines())
