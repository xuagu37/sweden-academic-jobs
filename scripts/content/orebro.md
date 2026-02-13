# Örebro University
<p style="font-size: 1.2em; font-weight: bold;">Total positions: 4</p>


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
<h3>Professor of Biology specialising in molecular physiology</h3>

- **Link:** [View job posting](https://www.oru.se/english/career/available-positions/job/?jid=20250355)
- **Department:** 
- **Published:** 
- **Deadline:** 2026-02-27

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>Doctoral student in Biology with specialisation in Toxicology</h3>

- **Link:** [View job posting](https://www.oru.se/english/career/available-positions/job/?jid=20260029)
- **Department:** 
- **Published:** 
- **Deadline:** 2026-03-04

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>Senior lecturers in Statistics</h3>

- **Link:** [View job posting](https://www.oru.se/english/career/available-positions/job/?jid=20260028)
- **Department:** 
- **Published:** 
- **Deadline:** 2026-03-06

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoctoral researchers in Computer Science, Cybersecurity</h3>

- **Link:** [View job posting](https://www.oru.se/english/career/available-positions/job/?jid=20260006)
- **Department:** 
- **Published:** 
- **Deadline:** 2026-03-11
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
