// Research Scout addition. This fills a local form and never starts research.
'use strict';
(async function loadScoutWorkflows() {
  const picker = document.getElementById('scout-workflow');
  const status = document.getElementById('scout-template-status');
  if (!picker) return;
  try {
    const response = await fetch('/site/scout-workflows.json');
    if (!response.ok) throw new Error('template load failed');
    const workflows = await response.json();
    for (const workflow of workflows) {
      const option = document.createElement('option');
      option.value = workflow.id;
      option.textContent = workflow.name;
      picker.appendChild(option);
    }
    picker.addEventListener('change', () => {
      const workflow = workflows.find(item => item.id === picker.value);
      const task = document.getElementById('task');
      if (!workflow || !task) return;
      if (task.value.trim() && !window.confirm('使用模板替换当前研究问题？')) { picker.value = ''; return; }
      task.value = workflow.task;
      for (const field of ['report_type', 'report_source']) {
        const control = document.querySelector(`[name="${field}"]`);
        if (control && [...control.options].some(option => option.value === workflow[field])) control.value = workflow[field];
      }
      task.dispatchEvent(new Event('input', {bubbles: true}));
      status.textContent = '模板已填入。请先替换 {{变量}}，再手动启动研究。';
      task.focus();
    });
  } catch (_) {
    status.textContent = '模板未加载，请查看仓库 scout/ 目录中的可复制版本。';
  }
})();
