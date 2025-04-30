import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import BasicExample from "../layouts/NavBar";
import Footer from "../layouts/Footer";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;
const WS_URL = import.meta.env.VITE_API_BASE_URL_WS;

const Manager = () => {
  const [images, setImages] = useState([]);
  const [title, setTitle] = useState("");
  const [newTitle, setNewTitle] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const socketRef = useRef(null);

  useEffect(() => {
    setupWebSocket();
  }, []);

  const handleTitleUpdate = async () => {
    const form = new FormData();
    form.append("new_title", newTitle);
    await axios.put(`${BASE_URL}/admin/title`, form);
    socketRef.current?.send(JSON.stringify({ action: "get_all" }));
  };

  const handleImageUpload = async () => {
    if (!imageFile) return;
    const form = new FormData();
    form.append("file", imageFile);
    await axios.post(`${BASE_URL}/admin/upload_image`, form);
    socketRef.current?.send(JSON.stringify({ action: "get_all" }));
  };

  const handleImageDelete = async (id) => {
    await axios.delete(`${BASE_URL}/admin/image/${id}`);
    socketRef.current?.send(JSON.stringify({ action: "get_all" }));
  };

  const setupWebSocket = () => {
    const socket = new WebSocket(WS_URL);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("✅ WebSocket connected");
      socket.send(JSON.stringify({ action: "get_all" }));
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === "full_data") {
        const data = message.data;
        if (data.images) setImages(data.images);
        if (data.title) {
          setTitle(data.title);
          setNewTitle(data.title);
        }
      }
    };

    socket.onclose = () => {
      console.log("❌ WebSocket disconnected");
    };
  };

  return (
    <div className="manager">
      <BasicExample />

      <div className="content">
        <h2>競賽題目</h2>
        <hr/>
        <textarea rows="2" cols="40" value={newTitle} onChange={(e) => setNewTitle(e.target.value)} 
          />
        <button onClick={handleTitleUpdate}>更新競賽題目</button>

        <p>
          目前競賽題目：<strong>{title}</strong>
        </p>

        <h2>圖片管理</h2>
        <hr/>
        <input type="file" onChange={(e) => setImageFile(e.target.files[0])} />
        <button onClick={handleImageUpload}>
          上傳圖片
        </button>

        <table
          border="1"
          cellPadding="10"
          style={{
            width: "100%",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr>
              <th>序</th>
              <th>編號</th>
              <th>圖片</th>
              <th>刪除</th>
            </tr>
          </thead>
          <tbody>
            {images.map((img, index) => (
              <tr key={img.id}>
                <td>{index + 1}</td>
                <td>{img.id}</td>
                <td>
                  <img
                    src={`${BASE_URL}${img.url}`}
                    alt={img.id}
                    style={{cursor: "pointer" }}
                    onClick={() =>
                      window.open(`${BASE_URL}${img.url}`, "_blank")
                    }
                  />
                </td>
                <td>
                  <button onClick={() => handleImageDelete(img.id)}>
                    刪除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Footer />
    </div>
  );
};

export default Manager;
