import { useState } from "react";
import { postFiles } from "../api/client";
import SectionCard from "../components/SectionCard";

export default function UploadPage() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [message, setMessage] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    if (!selectedFiles.length) {
      setMessage("请先选择日志文件。");
      return;
    }
    try {
      const result = await postFiles("/tasks/upload", selectedFiles);
      setMessage(`成功创建 ${result.length} 个评测任务。`);
      setSelectedFiles([]);
      event.target.reset();
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div className="page">
      <SectionCard title="上传 Agent 日志">
        <form className="upload-form" onSubmit={handleSubmit}>
          <input
            type="file"
            accept=".json"
            multiple
            onChange={(event) => setSelectedFiles(Array.from(event.target.files || []))}
          />
          <button type="submit">上传并创建评测任务</button>
        </form>
        <p className="tip">支持批量上传 JSON 格式 Trace Logs，系统会自动执行脱敏、解析与评分。</p>
        {message ? <p className="message">{message}</p> : null}
      </SectionCard>
    </div>
  );
}
