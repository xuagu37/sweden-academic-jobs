# Karlstad University
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

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD student positions in Mathematics Education</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:878246/iframeEmbedded:0/where:4)
- **Deadline:** 25.Feb.2026

</div>

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Doktorand i omvårdnad</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:887013/iframeEmbedded:0/where:4)
- **Deadline:** 28.Feb.2026

</div>

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Universitetsadjunkt i genusvetenskap, vikariat 100 %</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:898848/iframeEmbedded:0/where:4)
- **Deadline:** 01.Mar.2026

</div>

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Projektassistent forskning inom de samhällsvetenskapliga ämnenas didaktik</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:894726/iframeEmbedded:0/where:4)
- **Deadline:** 01.Mar.2026

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>Doctoral student in science education or technology education</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:888726/iframeEmbedded:0/where:4)
- **Deadline:** 01.Mar.2026

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>University lecturer in computer science with a specialisation in artificial intelligence (temporary position)</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:878594/iframeEmbedded:0/where:4)
- **Deadline:** 03.Mar.2026

</div>

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Amanuens i psykologi</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:893805/iframeEmbedded:0/where:4)
- **Deadline:** 04.Mar.2026

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoctoral Researcher in Computer Science with focus on High Quality Synthetic Data</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:895196/iframeEmbedded:0/where:4)
- **Deadline:** 08.Mar.2026

</div>

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Vikarierande universitetsadjunkt i matematik med inriktning mot didaktik</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:872584/iframeEmbedded:0/where:4)
- **Deadline:** 12.Mar.2026

</div>

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Projektkoordinator</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:895052/iframeEmbedded:0/where:4)
- **Deadline:** 15.Mar.2026

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>5 Doctoral Studentships in Subject-Specific Education</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:894655/iframeEmbedded:0/where:4)
- **Deadline:** 16.Mar.2026

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>Doctoral student in Computer Science at Karlstad University in cooperation with Cybercampus Sweden</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:887414/iframeEmbedded:0/where:4)
- **Deadline:** 16.Mar.2026

</div>

<div class="job" data-type="Other" style="margin-bottom: 1.5em;">
<h3>Utbildningshandläggare</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:906255/iframeEmbedded:0/where:4)
- **Deadline:** 16.Mar.2026

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>Senior lecturer in Gender Studies</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:898962/iframeEmbedded:0/where:4)
- **Deadline:** 22.Mar.2026

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>Doctoral student in Educational Work, specialising in Sports Science</h3>

- **Link:** [View job posting](https://kau.varbi.com/en/what:job/jobID:905516/iframeEmbedded:0/where:4)
- **Deadline:** 31.Mar.2026
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
