# Luleå University
<p style="font-size: 1.2em; font-weight: bold;">Total jobs: 12</p>


<div id="filters" style="margin: 1em 0;">
  <label for="filterType"><strong>Filter by Job Type:</strong></label>
  <select id="filterType" style="margin-right: 1em;">
    <option value="">Show All</option>
    <option value="PhD">PhD</option>
    <option value="Postdoc/Researcher">Postdoc/Researcher</option>
    <option value="Lecturer/Professor">Lecturer/Professor</option>
    <option value="Research Engineer">Research Engineer</option>    
    <option value="Other">Other</option>
  </select>
  <input type="text" id="jobFilter" placeholder="Search jobs..." style="padding: 0.5em; width: 50%;">
</div>

<div id="jobList">
<div class="job" data-type="None" style="margin-bottom: 1.5em;">

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>Professor/Head of Subject in Computer Science</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9705#item-9705)
- **Deadline:** 2026-03-12

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoc position in Process Metallurgy</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9977#item-9977)
- **Deadline:** 2026-03-16

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoc position in Structural Engineering</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9975#item-9975)
- **Deadline:** 2026-03-17

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Process Metallurgy</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=10013#item-10013)
- **Deadline:** 2026-03-19

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Ore Geology</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9996#item-9996)
- **Deadline:** 2026-03-24

</div>

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Amanuensis Machine Learning</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=10039#item-10039)
- **Deadline:** 2026-03-26

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>Professor of Cyber-Physical Systems</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=10042#item-10042)
- **Deadline:** 2026-03-27

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoc position in Structural Engineering</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9972#item-9972)
- **Deadline:** 2026-03-31

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Ore Geology</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9994#item-9994)
- **Deadline:** 2026-03-31

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoc position in Space Systems with focus on spacecraft avionics</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=10045#item-10045)
- **Deadline:** 2026-05-03

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Space Systems</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=10032#item-10032)
- **Deadline:** 2026-05-28

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Space Systems</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=10034#item-10034)
- **Deadline:** 2026-05-28
</div></div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  const typeSelect = document.getElementById('filterType');
  const textInput = document.getElementById('jobFilter');
  const jobBlocks = document.querySelectorAll('.job');

  function updateDisplay() {
    const selected = typeSelect.value.toLowerCase();
    const query = textInput.value.toLowerCase();

    jobBlocks.forEach(job => {
      const jobType = (job.dataset.type || "").toLowerCase();
      const matchesType = !selected || jobType === selected;
      const matchesQuery = job.textContent.toLowerCase().includes(query);
      job.style.display = (matchesType && matchesQuery) ? '' : 'none';
    });
  }

  typeSelect.addEventListener('change', updateDisplay);
  textInput.addEventListener('input', updateDisplay);
});
</script>
