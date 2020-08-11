FROM python:slim-buster

ARG PROXY
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

# User to run container
ARG USER_NAME
ARG USER_ID
ARG GROUP_ID
RUN if [ ! "${USER_NAME}" = "root" ] && [ ${USER_ID:-0} -ne 0 ] && [ ${GROUP_ID:-0} -ne 0 ]; then \
    if id "${USER_NAME}" >/dev/null 2>&1; then \
        userdel -r -f ${USER_NAME} \
    ;fi &&\
    if grep -q "^${USER_NAME}:" /etc/group; then \
        groupdel ${USER_NAME} \
    ;fi &&\
    groupadd -f -g ${GROUP_ID} ${USER_NAME} &&\
    useradd -m -l -u ${USER_ID} -g ${USER_NAME} ${USER_NAME}  &&\
    usermod --shell /bin/bash ${USER_NAME} &&\
    usermod -a -G root ${USER_NAME} &&\
    echo "${USER_NAME}:${USER_NAME}" |  chpasswd &&\
    echo 'export PS1="\u@ \[\e[32m\]\w\[\e[m\]\[\e[35m\]\[\e[m\]\\n$ "' \
        >> /home/${USER_NAME}/.bashrc &&\
    echo $USER_NAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER_NAME  &&\
    chmod 0440 /etc/sudoers.d/$USER_NAME \
    #chown -R ${USER_ID}:${GROUP_ID} /  > /dev/null 2>&1 ||:  \
;fi
USER ${USER_NAME}

# Install python packages
COPY ./*.py /tmp/src/
COPY ./requirements* /tmp/src/
COPY ./pyquick /tmp/src/pyquick
COPY ./LICENSE /tmp/src/
COPY ./README.md /tmp/src/
RUN cd /tmp/src &&\ 
    pip install -U --no-cache-dir -r /tmp/src/requirements.txt &&\
    pip install -U --upgrade pip &&\
    sudo python /tmp/src/setup.py install &&\
    cd &&\
    sudo rm -fr /tmp/src

ENTRYPOINT ["pyquick"]
