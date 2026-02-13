# Södertörn University
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

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Informationskoordinator</h3>

- **Link:** [View job posting](https://web103.reachmee.com/ext/I007/532/job?site=24&lang=UK&validator=2f5f4343b7f80edb4b210427ef968f34&ref=https%3A%2F%2Fwww.overleaf.com%2F&job_id=9525)
- **Department:** 
- **Published:** 
- **Deadline:** 2026-03-04

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Project-specific researcher at CBEES</h3>

- **Link:** [View job posting](https://web103.reachmee.com/ext/I007/532/job?site=24&lang=UK&validator=2f5f4343b7f80edb4b210427ef968f34&ref=https%3A%2F%2Fwww.overleaf.com%2F&job_id=9482)
- **Department:** 
- **Published:** 
- **Deadline:** 2026-02-27

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoctoral Research Fellow in Social Science at CBEES</h3>

- **Link:** [View job posting](https://web103.reachmee.com/ext/I007/532/job?site=24&lang=UK&validator=2f5f4343b7f80edb4b210427ef968f34&ref=https%3A%2F%2Fwww.overleaf.com%2F&job_id=9475)
- **Department:** 
- **Published:** 
- **Deadline:** 2026-02-27

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoctoral Research Fellow in Historical Studies at CBEES</h3>

- **Link:** [View job posting](https://web103.reachmee.com/ext/I007/532/job?site=24&lang=UK&validator=2f5f4343b7f80edb4b210427ef968f34&ref=https%3A%2F%2Fwww.overleaf.com%2F&job_id=9478)
- **Department:** 
- **Published:** 
- **Deadline:** 2026-02-27
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
