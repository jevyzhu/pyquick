FROM python:slim-buster

ARG PROXY="http://web-proxy.ap.softwaregrp.net:8080"
ENV HTTP_PROXY $PROXY
ENV HTTPS_PROXY $PROXY
ENV http_proxy $PROXY
ENV https_proxy $PROXY

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /etc/apt && touch /etc/apt/apt.conf \
    && echo "Acquire::http::proxy \"$PROXY\";" > /etc/apt/apt.conf \ 
    && echo "Acquire::https::proxy \"$PROXY\";" >> /etc/apt/apt.conf \ 
    && apt-get update && apt-get install -y sudo

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

# Install python packages
COPY . /src
RUN cd /src &&\ 
    pip install -U --no-cache-dir -r ./requirements.txt &&\
    pip install -U --upgrade pip &&\
    python ./setup.py install

# User to run container
ARG USER_ID
ARG GROUP_ID
ARG PROD_USER
RUN if [ ! "${PROD_USER}" = "root" ] && [ ${USER_ID:-0} -ne 0 ] && [ ${GROUP_ID:-0} -ne 0 ]; then \
    if id "${PROD_USER}" >/dev/null 2>&1; then \
        userdel -r -f ${PROD_USER} \
    ;fi &&\
    groupadd -f -g ${GROUP_ID} ${PROD_USER} &&\
    useradd -m -l -u ${USER_ID} -g ${PROD_USER} ${PROD_USER}  &&\
    usermod --shell /bin/bash ${PROD_USER} &&\
    usermod -a -G root ${PROD_USER} &&\
    echo "${PROD_USER}:${PROD_USER}" |  chpasswd &&\
    echo 'export PS1="\u@ \[\e[32m\]\w\[\e[m\]\[\e[35m\]\[\e[m\]\\n$ "' \
        >> /home/${PROD_USER}/.bashrc &&\
    echo $PROD_USER ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$PROD_USER  &&\
    chmod 0440 /etc/sudoers.d/$PROD_USER  &&\
    chown -R ${USER_ID}:${GROUP_ID} /  > /dev/null 2>&1 ||:  \
;fi
USER ${PROD_USER}

ENTRYPOINT ["pyquick"]
