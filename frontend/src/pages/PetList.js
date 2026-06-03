import React, { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { petsAPI } from '../api/api';
import { ADOPTION_STATUS } from '../constants/site';
import AdminManageBar from '../components/AdminManageBar';

const SPECIES_LABELS = {
  dog: '狗',
  cat: '猫',
  bird: '鸟',
  rabbit: '兔',
  fish: '鱼',
  other: '其他',
};

const GENDER_LABELS = {
  male: '公',
  female: '母',
  unknown: '未知',
};

const formatAgeMonths = (months) => {
  if (months == null || months === '') return '未知';
  const m = Number(months);
  if (m < 12) return `${m}个月`;
  const years = Math.floor(m / 12);
  const rem = m % 12;
  if (rem === 0) return `${years}岁`;
  return `${years}岁${rem}个月`;
};

const ADOPTION_BADGE = {
  available: 'success',
  pending: 'warning text-dark',
  adopted: 'secondary',
};

const PetList = () => {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();

  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [speciesFilter, setSpeciesFilter] = useState(searchParams.get('species') || '');

  useEffect(() => {
    const fetchPets = async () => {
      try {
        setLoading(true);
        const params = { adoption_status: 'available' };
        if (speciesFilter) params.species = speciesFilter;
        const response = await petsAPI.getAll(params);
        setPets(Array.isArray(response.data) ? response.data : response.data.results || []);
      } catch (err) {
        setError('加载宠物列表失败，请稍后重试。');
        console.error('Error fetching pets:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPets();
  }, [speciesFilter]);

  useEffect(() => {
    const params = new URLSearchParams();
    if (search) params.set('search', search);
    if (speciesFilter) params.set('species', speciesFilter);
    setSearchParams(params);
  }, [search, speciesFilter, setSearchParams]);

  const filteredPets = pets.filter((pet) => {
    if (!search) return true;
    return pet.name && pet.name.toLowerCase().includes(search.toLowerCase());
  });

  const hasActiveFilters = search || speciesFilter;

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-success" role="status">
          <span className="visually-hidden">加载中...</span>
        </div>
        <p className="mt-2">正在加载宠物列表...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        {error}
      </div>
    );
  }

  return (
    <div className="pet-list-container">
      <div className="search-filter-section mb-4">
        <div className="container">
          <div className="row g-3">
            <div className="col-md-5">
              <div className="search-box">
                <i className="fas fa-search search-icon"></i>
                <input
                  type="text"
                  className="form-control search-input"
                  placeholder="按名称搜索宠物..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>
            </div>
            <div className="col-md-4">
              <select
                className="form-select filter-select"
                value={speciesFilter}
                onChange={(e) => setSpeciesFilter(e.target.value)}
              >
                <option value="">全部种类</option>
                <option value="dog">狗</option>
                <option value="cat">猫</option>
                <option value="bird">鸟</option>
                <option value="rabbit">兔</option>
                <option value="fish">鱼</option>
                <option value="other">其他</option>
              </select>
            </div>
            <div className="col-md-3">
              <button
                className="btn btn-outline-secondary w-100"
                onClick={() => {
                  setSearch('');
                  setSpeciesFilter('');
                }}
                disabled={!hasActiveFilters}
              >
                清除筛选
              </button>
            </div>
          </div>

          {hasActiveFilters && (
            <div className="active-filters mt-3">
              <div className="d-flex flex-wrap gap-2">
                {search && (
                  <span className="badge bg-success d-flex align-items-center">
                    搜索：{search}
                    <button
                      type="button"
                      className="btn-close btn-close-white ms-2"
                      aria-label="移除搜索条件"
                      onClick={() => setSearch('')}
                    ></button>
                  </span>
                )}
                {speciesFilter && (
                  <span className="badge bg-primary d-flex align-items-center">
                    种类：{SPECIES_LABELS[speciesFilter] || speciesFilter}
                    <button
                      type="button"
                      className="btn-close btn-close-white ms-2"
                      aria-label="移除种类筛选"
                      onClick={() => setSpeciesFilter('')}
                    ></button>
                  </span>
                )}
                <span className="badge bg-info text-dark">状态：可领养</span>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="container mb-4">
        <h5 className="text-muted">
          共找到 {filteredPets.length} 只可领养宠物
        </h5>
      </div>

      <div className="container">
        <div className="row">
          {filteredPets.map((pet) => (
            <div key={pet.id} className="col-md-4 col-lg-3 mb-4">
              <div className="pet-card">
                <img
                  src={pet.photo_url || 'https://via.placeholder.com/300x200?text=Pet+Photo'}
                  className="pet-card-img"
                  alt={pet.name || '宠物'}
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/300x200?text=Pet+Photo';
                  }}
                />
                <div className="pet-card-body">
                  <AdminManageBar
                    onEdit={() => window.location.assign(`/pets/${pet.id}`)}
                    onHide={async () => {
                      await petsAPI.update(pet.id, { is_public: false });
                      window.location.reload();
                    }}
                    onDelete={async () => {
                      if (!window.confirm('确定删除？')) return;
                      await petsAPI.delete(pet.id);
                      window.location.reload();
                    }}
                  />
                  <h5 className="pet-card-title">
                    <i
                      className={`fas fa-${
                        pet.species === 'dog' ? 'dog' : pet.species === 'cat' ? 'cat' : 'paw'
                      } me-2 text-success`}
                    ></i>
                    {pet.name || '未命名宠物'}
                  </h5>
                  <p className="pet-card-text">
                    <strong>种类：</strong> {SPECIES_LABELS[pet.species] || pet.species || '未知'}
                    <br />
                    <strong>品种：</strong> {pet.breed || '未知'}
                    <br />
                    <strong>年龄：</strong> {formatAgeMonths(pet.age_months)}
                    <br />
                    <strong>性别：</strong> {GENDER_LABELS[pet.gender] || pet.gender || '未知'}
                    <br />
                    <strong>状态：</strong>{' '}
                    <span className={`badge ms-1 bg-${ADOPTION_BADGE[pet.adoption_status] || 'secondary'}`}>
                      {ADOPTION_STATUS[pet.adoption_status] || pet.adoption_status || '未知'}
                    </span>
                  </p>
                  <p className="pet-card-description">{pet.description || '暂无描述。'}</p>
                  <Link to={`/pets/${pet.id}`} className="btn btn-success w-100">
                    查看详情
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredPets.length === 0 && (
          <div className="text-center py-5">
            <i className="fas fa-search fa-3x text-muted mb-3"></i>
            <p className="text-muted">没有符合搜索条件的可领养宠物。</p>
          </div>
        )}
      </div>

      <style>{`
        .pet-list-container {
          background-color: #FAFAFA;
          min-height: 100vh;
          padding-top: 2rem;
        }
        .search-filter-section {
          background-color: white;
          border-radius: 15px;
          padding: 2rem;
          box-shadow: 0 4px 15px rgba(0,0,0,0.1);
          margin-bottom: 2rem;
        }
        .search-box { position: relative; }
        .search-icon {
          position: absolute;
          left: 15px;
          top: 50%;
          transform: translateY(-50%);
          color: #666;
          z-index: 10;
        }
        .search-input {
          padding-left: 45px;
          border-radius: 25px;
          border: 2px solid #e9ecef;
          transition: all 0.3s ease;
        }
        .search-input:focus {
          border-color: #00C897;
          box-shadow: 0 0 0 0.2rem rgba(0, 200, 151, 0.25);
        }
        .filter-select {
          border-radius: 25px;
          border: 2px solid #e9ecef;
          transition: all 0.3s ease;
        }
        .filter-select:focus {
          border-color: #00C897;
          box-shadow: 0 0 0 0.2rem rgba(0, 200, 151, 0.25);
        }
        .active-filters {
          padding: 1rem;
          background-color: #f8f9fa;
          border-radius: 10px;
        }
        .pet-card {
          background: white;
          border-radius: 15px;
          overflow: hidden;
          box-shadow: 0 4px 15px rgba(0,0,0,0.1);
          transition: all 0.3s ease;
          height: 100%;
        }
        .pet-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .pet-card-img {
          width: 100%;
          height: 200px;
          object-fit: cover;
        }
        .pet-card-body { padding: 1.5rem; }
        .pet-card-title { color: #333; margin-bottom: 1rem; }
        .pet-card-text { color: #666; font-size: 0.9rem; margin-bottom: 1rem; }
        .pet-card-description {
          color: #888;
          font-size: 0.85rem;
          margin-bottom: 1.5rem;
          line-height: 1.4;
        }
        .btn-success {
          background-color: #00C897;
          border-color: #00C897;
          border-radius: 25px;
          transition: all 0.3s ease;
        }
        .btn-success:hover {
          background-color: #00B386;
          border-color: #00B386;
          transform: translateY(-2px);
        }
      `}</style>
    </div>
  );
};

export default PetList;
