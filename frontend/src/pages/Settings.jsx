import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { updateMe, changePassword, deleteAccount } from '../api/auth'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import Modal from '../components/ui/Modal'

export default function Settings() {
  const { user, logout, updateUser } = useAuth()
  const navigate = useNavigate()

  const [profile, setProfile] = useState({ full_name: user?.full_name || '' })
  const [profileMsg, setProfileMsg] = useState('')
  const [profileLoading, setProfileLoading] = useState(false)

  const [passwords, setPasswords] = useState({ current_password: '', new_password: '' })
  const [passwordMsg, setPasswordMsg] = useState('')
  const [passwordLoading, setPasswordLoading] = useState(false)

  const [deleteModal, setDeleteModal] = useState(false)
  const [deleteLoading, setDeleteLoading] = useState(false)

  const handleProfileSave = async () => {
    setProfileLoading(true)
    setProfileMsg('')
    try {
      const res = await updateMe(profile)
      updateUser(res.data)
      setProfileMsg('Profile updated successfully')
    } catch (e) {
      setProfileMsg(e.response?.data?.detail || 'Failed to update profile')
    } finally {
      setProfileLoading(false)
    }
  }

  const handlePasswordChange = async () => {
    if (passwords.new_password.length < 8) {
      setPasswordMsg('New password must be at least 8 characters')
      return
    }
    setPasswordLoading(true)
    setPasswordMsg('')
    try {
      await changePassword(passwords)
      setPasswords({ current_password: '', new_password: '' })
      setPasswordMsg('Password changed successfully')
    } catch (e) {
      setPasswordMsg(e.response?.data?.detail || 'Failed to change password')
    } finally {
      setPasswordLoading(false)
    }
  }

  const handleDeleteAccount = async () => {
    setDeleteLoading(true)
    try {
      await deleteAccount()
      await logout()
      navigate('/login')
    } catch (e) {
      setDeleteLoading(false)
      setDeleteModal(false)
    }
  }

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Settings</h1>

      {/* Profile */}
      <section className="bg-white rounded-xl border border-gray-100 p-6 mb-6">
        <h2 className="font-semibold text-gray-900 mb-4">Profile</h2>
        <div className="space-y-4">
          <Input
            label="Full name"
            value={profile.full_name}
            onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
          />
          <Input label="Email" value={user?.email || ''} disabled className="opacity-60 cursor-not-allowed" />
          {profileMsg && (
            <p className={`text-sm ${profileMsg.includes('success') ? 'text-green-600' : 'text-red-600'}`}>
              {profileMsg}
            </p>
          )}
          <Button onClick={handleProfileSave} loading={profileLoading} size="sm">
            Save profile
          </Button>
        </div>
      </section>

      {/* Password */}
      <section className="bg-white rounded-xl border border-gray-100 p-6 mb-6">
        <h2 className="font-semibold text-gray-900 mb-4">Change Password</h2>
        <div className="space-y-4">
          <Input
            label="Current password"
            type="password"
            value={passwords.current_password}
            onChange={(e) => setPasswords({ ...passwords, current_password: e.target.value })}
          />
          <Input
            label="New password"
            type="password"
            placeholder="At least 8 characters"
            value={passwords.new_password}
            onChange={(e) => setPasswords({ ...passwords, new_password: e.target.value })}
          />
          {passwordMsg && (
            <p className={`text-sm ${passwordMsg.includes('success') ? 'text-green-600' : 'text-red-600'}`}>
              {passwordMsg}
            </p>
          )}
          <Button onClick={handlePasswordChange} loading={passwordLoading} size="sm">
            Update password
          </Button>
        </div>
      </section>

      {/* Danger zone */}
      <section className="bg-white rounded-xl border border-red-100 p-6">
        <h2 className="font-semibold text-red-700 mb-2">Danger Zone</h2>
        <p className="text-sm text-gray-500 mb-4">
          Deleting your account permanently removes all your journals, conversations, and data. This cannot be undone.
        </p>
        <Button variant="danger" size="sm" onClick={() => setDeleteModal(true)}>
          Delete my account
        </Button>
      </section>

      {/* Delete confirmation modal */}
      <Modal isOpen={deleteModal} onClose={() => setDeleteModal(false)} title="Delete Account">
        <p className="text-sm text-gray-600 mb-6">
          Are you absolutely sure? All your memories, journals, and conversations will be permanently deleted.
        </p>
        <div className="flex gap-3">
          <Button variant="secondary" onClick={() => setDeleteModal(false)} className="flex-1">
            Cancel
          </Button>
          <Button variant="danger" loading={deleteLoading} onClick={handleDeleteAccount} className="flex-1">
            Yes, delete everything
          </Button>
        </div>
      </Modal>
    </div>
  )
}
