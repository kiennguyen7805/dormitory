import { Navigate, Route, Routes } from 'react-router-dom'

import LoginPage from '../auth/LoginPage'
import { ProtectedRoute } from '../auth/ProtectedRoute'
import StudentHome from '../features/dashboard/StudentHome'
import ApplicationManagementPage from '../features/contracts/ApplicationManagementPage'
import MyHousingPage from '../features/contracts/MyHousingPage'
import StudentApplicationsPage from '../features/contracts/StudentApplicationsPage'
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
      <Route path="/admin/applications" element={<ApplicationManagementPage />} />
    </Route>
    <Route element={<ProtectedRoute roles={['Student']}><StudentLayout /></ProtectedRoute>}>
      <Route path="/student" element={<StudentHome />} />
      <Route path="/student/applications" element={<StudentApplicationsPage />} />
      <Route path="/student/my-housing" element={<MyHousingPage />} />
    </Route>
    <Route path="*" element={<Navigate to="/login" replace />} />
  </Routes>
}
