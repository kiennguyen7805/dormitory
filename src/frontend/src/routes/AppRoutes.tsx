import { Navigate, Route, Routes } from 'react-router-dom'

import LoginPage from '../auth/LoginPage'
import { ProtectedRoute } from '../auth/ProtectedRoute'
import StudentHome from '../features/dashboard/StudentHome'
import HousingPage from '../features/housing/HousingPage'
import RoomMatrix from '../features/housing/RoomMatrix'
import AdminLayout from '../layouts/AdminLayout'
import StudentLayout from '../layouts/StudentLayout'

export default function AppRoutes() {
  return <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route element={<ProtectedRoute roles={['Admin', 'Staff']}><AdminLayout /></ProtectedRoute>}>
      <Route path="/admin/housing" element={<HousingPage />} />
      <Route path="/admin/room-matrix" element={<RoomMatrix />} />
    </Route>
    <Route element={<ProtectedRoute roles={['Student']}><StudentLayout /></ProtectedRoute>}>
      <Route path="/student" element={<StudentHome />} />
    </Route>
    <Route path="*" element={<Navigate to="/login" replace />} />
  </Routes>
}
