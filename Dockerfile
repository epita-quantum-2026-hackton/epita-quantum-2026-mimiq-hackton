FROM python:3.13.11-trixie

RUN apt-get update && apt-get upgrade

RUN addgroup --gid 1000 mimiq \
  && adduser --uid 1000 --ingroup mimiq --home /home/mimiq --disabled-password mimiq

WORKDIR /home/mimiq/app

RUN chown 1000:1000 /home/mimiq/app

COPY --chown=mimiq:mimiq ./requirements.txt ./requirements.txt

RUN apt-get install -y \
  git \
  bash \
  g++ \
  make \
  cmake \
  && rm -rf /var/lib/apt/lists/* \
  && pip install -r requirements.txt --no-cache-dir --root-user-action=ignore \
  && jill install 1.12.4 --confirm \
  && python -c "import julia; julia.install();"

USER mimiq

RUN julia -e ' \
  using Pkg; \
  Pkg.Registry.add("General"); \
  Pkg.Registry.add(RegistrySpec(url="https://github.com/qperfect-io/QPerfectRegistry.git")); \
  Pkg.add(["IJulia", "MimiqCircuits"]);'

COPY --chown=mimiq:mimiq ./docker ./docker
COPY --chown=mimiq:mimiq ./src ./src

ENV PYTHONPATH=/home/mimiq/app/src

EXPOSE 8888

VOLUME [ "/home/mimiq/app/circuits" ]

ENTRYPOINT [ "bash", "/home/mimiq/app/docker/entrypoint.sh" ]
