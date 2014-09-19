# System wide functions and aliases for bash
#

# If not running interactively, don't do anything
if [[ $- != *i* ]] ; then
  return
fi

PS1="[\u@\h \W]\\$ "
PS2="> "
PS3="> "
PS4="+ "

case $TERM in
  gnome*|xterm*|rxvt*)
    PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME}: ${PWD}\007"'
    ;;
  *)
    ;;
esac

export SHELL='/usr/bin/bash'
