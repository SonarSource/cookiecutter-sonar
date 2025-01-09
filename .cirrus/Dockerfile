ARG CIRRUS_AWS_ACCOUNT

# Waiting for a fix: https://sonarsource.atlassian.net/browse/BUILD-5604
# hadolint ignore=DL3007
FROM ${CIRRUS_AWS_ACCOUNT}.dkr.ecr.eu-central-1.amazonaws.com/base:latest

USER root

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# sonar-scanner-cli
# renovate: datasource=github-releases depName=SonarSource/sonar-scanner-cli
ENV SONAR_SCANNER_CLI_VERSION=6.1.0.4477

RUN curl -L -O https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_CLI_VERSION}-linux-x64.zip && \
    unzip sonar-scanner-cli-${SONAR_SCANNER_CLI_VERSION}-linux-x64.zip
RUN mv sonar-scanner-${SONAR_SCANNER_CLI_VERSION}-linux-x64 /opt/sonar-scanner-cli && \
    chmod a+x /opt/sonar-scanner-cli/bin/sonar-scanner

USER sonarsource

COPY ../.tool-versions /home/sonarsource/
RUN echo 'eval "$(mise activate bash --shims)"' >> ~/.bashrc && \
    eval "$(mise activate bash --shims)" && \
    mise use -g python && \
