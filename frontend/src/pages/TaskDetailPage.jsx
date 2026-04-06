import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getJson } from "../api/client";
import SectionCard from "../components/SectionCard";

function renderNode(node) {
  return (
    <li key={node.id}>
      <strong>{node.title}</strong>
      <p>{node.content || "无内容"}</p>
      {node.tool_name ? <span className="chip">{node.tool_name}</span> : null}
      {node.children?.length ? <ul>{node.children.map(renderNode)}</ul> : null}
    </li>
  );
}

export default function TaskDetailPage() {
  const { taskId } = useParams();
  const [task, setTask] = useState(null);

  useEffect(() => {
    getJson(`/tasks/${taskId}`).then(setTask).catch(console.error);
  }, [taskId]);

  if (!task) {
    return <div className="page"><p>正在加载任务详情...</p></div>;
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Task Detail</p>
          <h2>{task.name}</h2>
        </div>
        <span className={`status status-${task.status}`}>{task.status}</span>
      </div>

      <div className="two-column">
        <SectionCard title="评分结果">
          {task.score_result ? (
            <div className="score-grid">
              <div><span>准确性</span><strong>{task.score_result.accuracy}</strong></div>
              <div><span>逻辑连贯性</span><strong>{task.score_result.logic_consistency}</strong></div>
              <div><span>工具效率</span><strong>{task.score_result.tool_efficiency}</strong></div>
              <div><span>安全性</span><strong>{task.score_result.safety}</strong></div>
              <div><span>总分</span><strong>{task.score_result.total_score}</strong></div>
              <div><span>结论</span><strong>{task.score_result.verdict}</strong></div>
            </div>
          ) : <p>该任务尚未完成评分。</p>}
        </SectionCard>

        <SectionCard title="运行指标">
          {task.metrics ? (
            <div className="score-grid">
              <div><span>耗时</span><strong>{task.metrics.processing_seconds}s</strong></div>
              <div><span>Token</span><strong>{task.metrics.token_consumption}</strong></div>
              <div><span>成功率</span><strong>{task.metrics.success_rate}</strong></div>
              <div><span>BadCase</span><strong>{String(task.metrics.bad_case)}</strong></div>
            </div>
          ) : <p>暂无运行指标。</p>}
        </SectionCard>
      </div>

      <SectionCard title="裁判分析">
        <p>{task.score_result?.summary || "暂无总结。"}</p>
        <pre>{task.score_result?.chain_of_thought || "暂无 CoT 分析。"}</pre>
      </SectionCard>

      <SectionCard title="轨迹树回放">
        {task.parsed_trace?.roots ? (
          <ul className="trace-tree">{task.parsed_trace.roots.map(renderNode)}</ul>
        ) : <p>该任务尚未完成轨迹解析。</p>}
      </SectionCard>
    </div>
  );
}
