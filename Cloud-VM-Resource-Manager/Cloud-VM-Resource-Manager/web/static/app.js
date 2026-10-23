const $ = id => document.getElementById(id);
async function api(url, options={}) { const r=await fetch(url,{headers:{"Content-Type":"application/json"},...options}); const d=await r.json(); if(!r.ok) throw new Error(d.error||"Request failed"); return d; }
function toast(msg){const t=$("toast");t.textContent=msg;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),2600)}
function bar(value,kind=""){return `<span class="meter ${kind}"><span style="width:${value}%"></span></span><span class="pct">${value}%</span>`}
function render(vms){
 const running=vms.filter(v=>v.status==="Running"), stopped=vms.length-running.length;
 $("total").textContent=vms.length;$("running").textContent=running.length;$("stopped").textContent=stopped;
 $("avgcpu").textContent=(running.length?(running.reduce((a,v)=>a+v.cpu,0)/running.length):0).toFixed(1)+"%";
 $("count").textContent=vms.length+" instances";
 $("vmrows").innerHTML=vms.map(v=>`<tr><td><span class="vm-name">${esc(v.name)}</span><span class="vm-os">${esc(v.os)} · ${v.id}</span></td><td class="config">${v.cpu_cores} vCPU · ${v.ram_gb} GB RAM · ${v.disk_gb} GB</td><td>${bar(v.cpu)}</td><td>${bar(v.ram,"ram")}</td><td><span class="status ${v.status}">${v.status}</span></td><td><div class="actions">${v.status==="Running"?`<button class="action" onclick="act('${v.id}','stop')">Stop</button><button class="action" onclick="act('${v.id}','restart')">Restart</button>`:`<button class="action" onclick="act('${v.id}','start')">Start</button>`}</div></td></tr>`).join("");
 const insights=[];
 vms.filter(v=>v.status==="Running"&&v.cpu<20&&v.ram<35).forEach(v=>insights.push(`<div class="insight warning"><b>⚡ Possible underutilization: ${esc(v.name)}</b>CPU ${v.cpu}% and RAM ${v.ram}%. Review whether its allocated resources can be reduced.</div>`));
 vms.filter(v=>v.status==="Running"&&(v.cpu>80||v.ram>85)).forEach(v=>insights.push(`<div class="insight warning"><b>⚠ High resource usage: ${esc(v.name)}</b>Check workload demand; consider scaling resources or distributing traffic.</div>`));
 if(!insights.length)insights.push(`<div class="insight good"><b>✓ No immediate optimization flags</b>Current simulated resource levels do not cross the configured thresholds.</div>`);
 insights.push(`<div class="insight good"><b>ℹ Optimization is advisory</b>Recommendations are rule-based examples, not automatic changes to a real cloud account.</div>`);
 $("insight-list").innerHTML=insights.join("");
}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
async function refresh(){try{render(await api("/api/vms"))}catch(e){toast(e.message)}}
async function act(id,action){try{const d=await api(`/api/vms/${id}/action`,{method:"POST",body:JSON.stringify({action})});toast(d.message);refresh()}catch(e){toast(e.message)}}
function openModal(){$("modal").classList.add("show")}
function closeModal(){$("modal").classList.remove("show")}
async function addVM(e){e.preventDefault();try{const d=await api("/api/vms",{method:"POST",body:JSON.stringify({name:$("vmname").value,os:$("os").value,cpu_cores:$("cores").value,ram_gb:$("ram").value,disk_gb:$("disk").value})});closeModal();e.target.reset();toast(`${d.name} created (stopped)`);refresh()}catch(err){toast(err.message)}}
refresh();setInterval(refresh,3500);
