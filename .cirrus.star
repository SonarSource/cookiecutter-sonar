load("github.com/SonarSource/cirrus-modules@master", "load_features")

def main(ctx):
    return load_features(ctx, only_if=dict())
