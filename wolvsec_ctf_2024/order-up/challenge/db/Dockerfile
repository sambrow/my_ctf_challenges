FROM postgres:16.2
ENV POSTGRES_PASSWORD=secret94337655343
ENV POSTGRES_USER=username
ENV POSTGRES_DB=database

# flag 4
RUN FLAG_FILE=`mktemp /flag_XXXXXXXXXXXXXX.txt` && echo 'wctf{r34d1ng_f1l3s_1s_fun_297562356234324}' > $FLAG_FILE && chmod 444 $FLAG_FILE


# flag 5
RUN ROOT_FLAG_FILE=`mktemp /root_flag_XXXXXXXXXXXXXX.txt` && echo 'wctf{0nly_r00t_c4n_r34d_th15_836330971512343}' > $ROOT_FLAG_FILE && chmod 400 $ROOT_FLAG_FILE

# set SUID bit on /bin/cat so that it can be used by the postgres user to
# output the content of the ROOT_FLAG_FILE
# Getting this flag would prove that RCE had been achieved.
RUN chmod u+s /bin/cat
