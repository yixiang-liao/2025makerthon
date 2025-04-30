// routes/index.jsx
import { Routes, Route } from 'react-router-dom';
import Manager from '../pages/manager';
import Podcast from '../pages/podcast';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/Manager" element={<Manager />} />
      <Route path="/Podcast" element={<Podcast />} />
    </Routes>
  );
};

export default AppRoutes;
