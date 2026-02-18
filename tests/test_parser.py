from swedjobs.parser import parse_jobs_lund, parse_jobs_uppsala, parse_jobs_stockholm, parse_jobs_gothenburg, parse_jobs_ki, parse_jobs_kth, parse_jobs_linkoping, parse_jobs_umea, parse_jobs_orebro, parse_jobs_lulea, parse_jobs_malmo, parse_jobs_chalmers, parse_jobs_slu, parse_jobs_karlstad, parse_jobs_sodertorn, parse_jobs_dalarna, parse_jobs_gavle, parse_jobs_malardalen, parse_jobs_miun

def test_parser():
    test_file = "data/cache/latest_slu_page.html"
    jobs = parse_jobs_slu(test_file)

    print(f"\nTest complete: {len(jobs)} job(s) found.\n")

    for i, job in enumerate(jobs, 1):
        print(f"--- Job {i} ---")
        print(f"Title     : {job['title']}")
        print(f"URL       : {job['url']}")
        # print(f"Department: {job['department']}")
        # print(f"Published : {job['published']}")
        print(f"Deadline  : {job['deadline']}\n")

if __name__ == "__main__":
    test_parser()
