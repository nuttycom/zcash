FROM ubuntu:16.04
LABEL Description="Ubuntu 16.04 for zcash compilation"

RUN apt-get update && apt-get install -y git g++ build-essential cmake wget curl \
    software-properties-common autoconf automake pkg-config libc6-dev m4 g++-multilib \
    libtool ncurses-dev unzip python python-zmq zlib1g-dev curl bsdmainutils mingw-w64 git

RUN update-alternatives --set x86_64-w64-mingw32-gcc /usr/bin/x86_64-w64-mingw32-gcc-posix && \
    update-alternatives --set x86_64-w64-mingw32-g++ /usr/bin/x86_64-w64-mingw32-g++-posix

RUN mkdir ~/.cargo && \
    echo "[target.x86_64-pc-windows-gnu]" >> ~/.cargo/config && \
    echo "linker = \"x86_64-w64-mingw32-gcc\"" >> ~/.cargo/config && \
    echo "ar = \"x86_64-w64-mingw32-gcc-ar\""  >> ~/.cargo/config

RUN cd /opt && git clone https://github.com/adityapk00/zcash.git zcash-build && cd zcash-build && \
    git worktree add --detach ../zcash-linux origin/zecwallet-build && \
    git worktree add --detach ../zcash-win origin/zecwallet-build
