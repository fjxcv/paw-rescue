# -*- coding: utf-8 -*-
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'frontend/src/pages/PetList.js'
text = path.read_text(encoding='utf-8')

text = text.replace(
    "import AdminManageBar from '../components/AdminManageBar';\n",
    "import AdminManageBar from '../components/AdminManageBar';\nimport { useManageMode } from '../context/ManageModeContext';\n",
)

text = text.replace(
    "const PetList = () => {\n  const navigate = useNavigate();\n",
    "const PetList = () => {\n  const navigate = useNavigate();\n  const { canManage } = useManageMode();\n",
)

old_fetch = """  useEffect(() => {
    const fetchPets = async () => {
      try {
        setLoading(true);
        setError(null);
        const params = buildApiParams();
        const response = await petsAPI.getAll(params);
        setPets(Array.isArray(response.data) ? response.data : response.data.results || []);
      } catch (err) {
        setError('\u52a0\u8f7d\u5ba0\u7269\u5217\u8868\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\u3002');
        console.error('Error fetching pets:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPets();
  }, [speciesFilter, genderFilter, ageRangeFilter, locationFilter, search, buildApiParams]);"""

new_fetch = """  const fetchPets = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const params = buildApiParams();
      const response = await petsAPI.getAll(params);
      setPets(Array.isArray(response.data) ? response.data : response.data.results || []);
    } catch (err) {
      setError('\u52a0\u8f7d\u5ba0\u7269\u5217\u8868\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\u3002');
      console.error('Error fetching pets:', err);
    } finally {
      setLoading(false);
    }
  }, [buildApiParams]);

  useEffect(() => {
    fetchPets();
  }, [fetchPets]);"""

if old_fetch not in text:
    raise SystemExit('fetch block not found')
text = text.replace(old_fetch, new_fetch)

old_card = """                <div className=\"pet-card-img-wrapper\">
                  <img
                    src={pet.photo_url || 'https://via.placeholder.com/300x200?text=Pet+Photo'}
                    className=\"pet-card-img\"
                    alt={pet.name || '\u5ba0\u7269'}
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/300x200?text=Pet+Photo';
                    }}
                  />
                  <span className={`pet-status-badge badge bg-${ADOPTION_BADGE[pet.adoption_status] || 'secondary'}`}>
                    {ADOPTION_STATUS[pet.adoption_status] || '\u672a\u77e5'}
                  </span>
                </div>

                <div className=\"pet-card-body\">
                  {/* \u7ba1\u7406\u5458\u64cd\u4f5c\u680f \u2014 \u963b\u6b62\u5192\u6ce1\u9632\u6b62\u89e6\u53d1\u5361\u7247\u70b9\u51fb\u8df3\u8f6c */}
                  <div onClick={(e) => e.stopPropagation()}>
                    <AdminManageBar
                      onEdit={() => window.location.assign(`/pets/${pet.id}`)}
                      onHide={async () => {
                        await petsAPI.update(pet.id, { is_public: false });
                        window.location.reload();
                      }}
                      onDelete={async () => {
                        if (!window.confirm('\u786e\u5b9a\u5220\u9664\uff1f')) return;
                        await petsAPI.delete(pet.id);
                        window.location.reload();
                      }}
                    />
                  </div>"""

new_card = """                <div className=\"pet-card-img-wrapper\">
                  <img
                    src={pet.photo_url || 'https://via.placeholder.com/300x200?text=Pet+Photo'}
                    className=\"pet-card-img\"
                    alt={pet.name || '\u5ba0\u7269'}
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/300x200?text=Pet+Photo';
                    }}
                  />
                </div>

                <div className=\"pet-card-body\">
                  <div
                    className=\"d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2\"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <div className=\"d-flex align-items-center gap-1 flex-wrap\">
                      <span className={`badge bg-${ADOPTION_BADGE[pet.adoption_status] || 'secondary'}`}>
                        {ADOPTION_STATUS[pet.adoption_status] || '\u672a\u77e5'}
                      </span>
                      {canManage && !pet.is_public && (
                        <span className=\"badge bg-secondary\">\u672a\u516c\u5f00</span>
                      )}
                    </div>
                    <div className=\"flex-grow-1\">
                      <AdminManageBar
                        compact
                        onEdit={() => window.location.assign(`/pets/${pet.id}`)}
                        onHide={async () => {
                          try {
                            await petsAPI.update(pet.id, { is_public: false });
                            alert('\u5df2\u8bbe\u4e3a\u4e0d\u516c\u5f00');
                            fetchPets();
                          } catch (err) {
                            alert(err.response?.data?.detail || '\u64cd\u4f5c\u5931\u8d25');
                          }
                        }}
                        onDelete={async () => {
                          if (!window.confirm('\u786e\u5b9a\u5220\u9664\uff1f')) return;
                          try {
                            await petsAPI.delete(pet.id);
                            fetchPets();
                          } catch (err) {
                            alert(err.response?.data?.detail || '\u5220\u9664\u5931\u8d25');
                          }
                        }}
                      />
                    </div>
                  </div>"""

if old_card not in text:
    raise SystemExit('card block not found')
text = text.replace(old_card, new_card)
path.write_text(text, encoding='utf-8', newline='\n')
print('petlist patched')
