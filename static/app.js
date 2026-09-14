const tasks = document.querySelector('#tasks');
const filter = document.querySelector('#filter');

async function loadTasks() {
  const suffix = filter.value ? `?status=${filter.value}` : '';
  const response = await fetch(`/api/tasks${suffix}`);
  const data = await response.json();
  tasks.innerHTML = data.map(t => `<article class="task"><div><h3>${escapeHtml(t.title)}</h3><p>${escapeHtml(t.description || '')}</p></div><select onchange="changeStatus(${t.id}, this.value)"><option value="todo" ${t.status==='todo'?'selected':''}>To do</option><option value="in_progress" ${t.status==='in_progress'?'selected':''}>In progress</option><option value="done" ${t.status==='done'?'selected':''}>Done</option></select><button onclick="removeTask(${t.id})">Delete</button></article>`).join('') || '<p>No tasks yet.</p>';
}

document.querySelector('#task-form').addEventListener('submit', async e => {
  e.preventDefault();
  await fetch('/api/tasks', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({title:title.value, description:description.value})});
  e.target.reset(); loadTasks();
});
filter.addEventListener('change', loadTasks);
async function changeStatus(id, status) { await fetch(`/api/tasks/${id}`, {method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify({status})}); loadTasks(); }
async function removeTask(id) { await fetch(`/api/tasks/${id}`, {method:'DELETE'}); loadTasks(); }
function escapeHtml(value) { return value.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c])); }
loadTasks();
