import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getJson } from "../api/client";
import SectionCard from "../components/SectionCard";

export default function BadCasePage() {
  const [badCases, setBadCases] = useState([]);

  useEffect(() => {
    getJson("/dashboard/overview").then((data) => setBadCases(data.bad_cases)).catch(console.error);
  }, []);

  return (
    <div className="page">
      <SectionCard title="BadCase 低分案例分析">
        <div className="list">
          {badCases.length === 0 ? <p>当前没有低分任务。</p> : badCases.map((item) => (
            <div key={item.task_id} className="list-row">
              <Link to={`/tasks/${item.task_id}`}>{item.task_name}</Link>
              <span>{item.summary}</span>
              <strong>{item.total_score}</strong>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
