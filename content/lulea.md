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

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoc position in Robotics and Artificial Intelligence</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9826)
- **Deadline:** 

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoc position in Robotics and Artificial Intelligence</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9828)
- **Deadline:** 

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>Professor of Cyber-Physical Systems</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9742)
- **Deadline:** 

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>Associate Professor of Cyber-Physical Systems</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9748)
- **Deadline:** 

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoc position in Space Systems with focus on spacecraft avionics</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9783)
- **Deadline:** 

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD student in Biochemical Process Engineering</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9780)
- **Deadline:** 

</div>

<div class="job" data-type="Lecturer/Professor" style="margin-bottom: 1.5em;">
<h3>Senior Lecturer in Machine Learning</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9842)
- **Deadline:** 

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Mineral Processing</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9786)
- **Deadline:** 

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Urban Water Engineering – climate change effects and adaptation in urban streams</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9797)
- **Deadline:** 

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Urban Water Engineering – Stormwater sediment: from risk to resource</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9800)
- **Deadline:** 

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Urban Water Engineering – hydrological dynamics in nature-based stormwater solutions</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9806)
- **Deadline:** 

</div>

<div class="job" data-type="Research Engineer" style="margin-bottom: 1.5em;">
<h3>Senior Research Engineer in Robotics and Artificial Intelligence</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9862)
- **Deadline:** 

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Robotics and Artificial Intelligence</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9860)
- **Deadline:** 

</div>

<div class="job" data-type="PhD" style="margin-bottom: 1.5em;">
<h3>PhD Student in Robotics and Artificial Intelligence</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9864)
- **Deadline:** 

</div>

<div class="job" data-type="Postdoc/Researcher" style="margin-bottom: 1.5em;">
<h3>Postdoctoral position in Applied Geochemistry</h3>

- **Link:** [View job posting](https://www.ltu.se/en/about-ltu/work-at-ltu/vacant-positions#item-9695)
- **Deadline:**
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
