# Mid Sweden University
<p style="font-size: 1.2em; font-weight: bold;">Total jobs: 4</p>


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

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoctoral Researcher in Wireless Network Security and Trustworthy AI</h3>

- **Link:** [View job posting](https://www.miun.se/en/work-at-the-university/career/jobs/vacancy/postdoctoral-researcher-in-wireless--network-security-and-trustworthy-ai/)
- **Deadline:** 260304

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>A doctoral (PhD) student in Computer Engineering with focus on Visual AI</h3>

- **Link:** [View job posting](https://www.miun.se/en/work-at-the-university/career/jobs/vacancy/a-doctoral-phd-student-in-computer-engineering-with-focus-on-visual-ai/)
- **Deadline:** 260218

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD candidate in Sport Science - focus on cross-country skiing and biathlon</h3>

- **Link:** [View job posting](https://www.miun.se/en/work-at-the-university/career/jobs/vacancy/phd-candidate-in-sport-science---focus-on-cross-country-skiing-and-biathlon/)
- **Deadline:** 260220

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD candidate in Sport Science - focus on athlete health and performance</h3>

- **Link:** [View job posting](https://www.miun.se/en/work-at-the-university/career/jobs/vacancy/phd-candidate-in-sport-science---focus-on-athlete-health-and-performance/)
- **Deadline:** 260220
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
