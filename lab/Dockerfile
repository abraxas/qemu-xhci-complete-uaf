# syntax=docker/dockerfile:1.4
FROM debian:sid-slim

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    ASAN_OPTIONS=abort_on_error=1:halt_on_error=1:detect_leaks=0:allocator_may_return_null=1 \
    UBSAN_OPTIONS=halt_on_error=0:print_stacktrace=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bison \
        build-essential \
        ca-certificates \
        flex \
        git \
        libfdt-dev \
        libglib2.0-dev \
        libpixman-1-dev \
        meson \
        ninja-build \
        pkg-config \
        python3 \
        python3-setuptools \
        python3-venv \
        python3-wheel \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Pin v11.1.2 / 4fc49f46dc95d4a27de2509e7fceb2931e91faeb from github.com/qemu/QEMU.
ARG QEMU_PIN=4fc49f46dc95d4a27de2509e7fceb2931e91faeb
ARG QEMU_TAG=v11.1.2
RUN set -eux; \
    ok=0; \
    for attempt in 1 2 3; do \
      if git clone --depth 1 --branch "${QEMU_TAG}" https://github.com/qemu/QEMU.git /opt/qemu-src; then \
        ok=1; \
        break; \
      fi; \
      rm -rf /opt/qemu-src; \
      sleep 8; \
    done; \
    test "${ok}" = 1; \
    cd /opt/qemu-src; \
    HEAD="$(git rev-parse HEAD)"; \
    case "${HEAD}" in \
      "${QEMU_PIN}"*) ;; \
      *) git fetch --depth 1 origin "${QEMU_PIN}"; git checkout "${QEMU_PIN}" ;; \
    esac; \
    test -s /opt/qemu-src/VERSION; \
    grep -qx '11.1.2' /opt/qemu-src/VERSION

RUN mkdir -p /opt/qemu-build \
    && cd /opt/qemu-build \
    && /opt/qemu-src/configure \
        --prefix=/opt/qemu \
        --target-list=x86_64-softmmu \
        --enable-asan \
        --disable-docs \
        --disable-user \
        --disable-tools \
        --disable-guest-agent \
        --disable-werror \
    && ninja -C /opt/qemu-build qemu-system-x86_64 \
    && mkdir -p /opt/qemu/bin /opt/qemu/share \
    && cp /opt/qemu-build/qemu-system-x86_64 /opt/qemu/bin/qemu-system-x86_64 \
    && cp -a /opt/qemu-src/pc-bios /opt/qemu/share/qemu \
    && test -x /opt/qemu/bin/qemu-system-x86_64 \
    && /opt/qemu/bin/qemu-system-x86_64 --version | grep -F '11.1.2'

COPY entrypoint.sh /opt/qemu/entrypoint.sh
RUN chmod 0755 /opt/qemu/entrypoint.sh

WORKDIR /opt/qemu
EXPOSE 18700 18701
CMD ["/opt/qemu/entrypoint.sh"]
