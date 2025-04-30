import React, { useEffect, useState, useRef } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";

const WS_URL = import.meta.env.VITE_API_BASE_URL_WS;
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const Podcast = () => {
  const [images, setImages] = useState([]);
  const [title, setTitle] = useState("");
  const [displayItems, setDisplayItems] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const wsRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("✅ WebSocket connected");
      ws.send(JSON.stringify({ action: "get_all" }));
    };

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === "full_data") {
        const data = msg.data;

        if (data.images) setImages(data.images);
        if (data.title) setTitle(data.title);

        const customOrder = ["3D列印", "機工", "木工", "噴漆室"];
        const ordered = [];

        if (data.equipment_data) {
          for (const name of customOrder) {
            const found = data.equipment_data.find((d) => d.類別 === name);
            if (found) {
              ordered.push({ type: "equipment", data: found });
            }
          }
        }

        if (data.tool_data) {
          ordered.push({ type: "tool", data: data.tool_data });
        }

        setDisplayItems(ordered);
        setCurrentIndex(0);
      }
    };

    ws.onclose = () => console.log("❌ WebSocket disconnected");

    return () => ws.close();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % displayItems.length);
    }, 10000);
    return () => clearInterval(interval);
  }, [displayItems]);

  return (
    <div className="podcast">
      <div className="top">
        <img
          src="https://makerthon.nkust.edu.tw/site/themes/default/cht/images/logo_f.svg"
          alt="logo"
        />
      </div>

      <div className="group">
        <div className="img-group">
          <Swiper modules={[Navigation]} navigation loop className="mySwiper">
            {images.map((img) => (
              <SwiperSlide key={img.id}>
                <img src={`${BASE_URL}${img.url}`} alt={img.id} />
              </SwiperSlide>
            ))}
          </Swiper>
        </div>

        <div className="table-group">
          <table>
            {displayItems.length > 0 && (
              <>
                {displayItems[currentIndex].type === "equipment" && (
                  <>
                    <thead>
                      <tr>
                        <th colSpan="2" className="head">
                          {displayItems[currentIndex].data.類別}
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td className="label">可使用</td>
                        <td>{displayItems[currentIndex].data.正取 || "—"}</td>
                      </tr>
                      <tr>
                        <td className="label">候補中</td>
                        <td>{displayItems[currentIndex].data.備取 || "—"}</td>
                      </tr>
                    </tbody>
                  </>
                )}

                {displayItems[currentIndex].type === "tool" && (
                  <>
                    <thead>
                      <tr>
                        <th colSpan="2" className="head">
                          材料室 可領取名單
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td colSpan="2" className="data">
                          {displayItems[currentIndex].data}
                        </td>
                      </tr>
                    </tbody>
                  </>
                )}
              </>
            )}
          </table>
          <p>以上名單僅供參考，詳情請至租借系統查看。</p>
        </div>
      </div>

      <div className="bottom">
        <div className="title">{title}</div>
      </div>
    </div>
  );
};

export default Podcast;
