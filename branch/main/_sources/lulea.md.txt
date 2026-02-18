# Luleå University
<p style="font-size: 1.2em; font-weight: bold;">Total jobs: 15</p>


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
<h3>Senior Lecturer in Machine Learning</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9842#item-9842)
- **Deadline:** 2026-02-18

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Mineral Processing</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9786#item-9786)
- **Deadline:** 2026-02-22

</div>

<div class="job" data-type="Research Engineer" style="margin-bottom: 1.5em;">
<h3>Senior Research Engineer in Robotics and Artificial Intelligence</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9862#item-9862)
- **Deadline:** 2026-02-23

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Robotics and Artificial Intelligence</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9864#item-9864)
- **Deadline:** 2026-02-24

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Robotics and Artificial Intelligence</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9860#item-9860)
- **Deadline:** 2026-02-24

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Students in Process Metallurgy</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9853#item-9853)
- **Deadline:** 2026-02-28

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoctoral position in Applied Geochemistry</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9695#item-9695)
- **Deadline:** 2026-02-28

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Urban Water Engineering – hydrological dynamics in nature-based stormwater solutions</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9806#item-9806)
- **Deadline:** 2026-03-01

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Urban Water Engineering – Stormwater sediment: from risk to resource</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9800#item-9800)
- **Deadline:** 2026-03-01

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Urban Water Engineering – climate change effects and adaptation in urban streams</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9797#item-9797)
- **Deadline:** 2026-03-01

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoc in computational modeling of electrochemical C-H activa-tion</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9866#item-9866)
- **Deadline:** 2026-03-01

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>Professor/Head of Subject of Fire Technology</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9701#item-9701)
- **Deadline:** 2026-03-02

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Soil Mechanics</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9945#item-9945)
- **Deadline:** 2026-03-03

</div>

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Amanuensis in Robotics and Artificial Intelligence</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9949#item-9949)
- **Deadline:** 2026-03-03

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>Professor/Head of Subject in Computer Science</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies?rmjob=9705#item-9705)
- **Deadline:** 2026-03-12
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
