import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { deleteResource, getJson, postJson } from "../api/client";
import SectionCard from "../components/SectionCard";

export default function TasksPage() {
  const [tasks, setTasks] = useState([]);

  const loadTasks = () => getJson("/tasks").then(setTasks).catch(console.error);

  useEffect(() => {
    loadTasks();
  }, []);

  async function handleRerun(taskId) {
    await postJson(`/tasks/${taskId}/run`);
    loadTasks();
  }

  async function handleDelete(taskId) {
    await deleteResource(`/tasks/${taskId}`);
    loadTasks();
  }

  return (
    <div className="page">
      <SectionCard title="评测任务管理">
        <div className="table">
          <div className="table-head">
            <span>任务</span>
            <span>状态</span>
            <span>文件</span>
            <span>操作</span>
          </div>
          {tasks.map((task) => (
            <div key={task.id} className="table-row">
              <Link to={`/tasks/${task.id}`}>{task.name}</Link>
              <span className={`status status-${task.status}`}>{task.status}</span>
              <span>{task.file_name}</span>
              <div className="actions">
                <button onClick={() => handleRerun(task.id)}>重跑</button>
                <button className="ghost" onClick={() => handleDelete(task.id)}>删除</button>
              </div>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
