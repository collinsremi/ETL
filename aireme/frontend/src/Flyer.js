import { useRef, useEffect, useState } from 'react'
import html2canvas from 'html2canvas'

const UNSPLASH_KEY = process.env.REACT_APP_UNSPLASH_KEY

function getSearchQuery(propertyType, features) {
  if (features?.toLowerCase().includes('pool')) return 'luxury villa swimming pool'
  if (propertyType?.toLowerCase().includes('duplex')) return 'modern duplex house exterior'
  if (propertyType?.toLowerCase().includes('mansion')) return 'luxury mansion exterior'
  if (propertyType?.toLowerCase().includes('apartment')) return 'modern apartment building exterior'
  return 'luxury real estate house exterior'
}

export default function Flyer({ data, output }) {
  const flyerRef = useRef()
  const [photo, setPhoto] = useState(null)
  const [photoLoading, setPhotoLoading] = useState(true)

  useEffect(() => {
    const query = getSearchQuery(data.property_type, data.features)
    fetch(`https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&orientation=landscape&per_page=1&client_id=${UNSPLASH_KEY}`)
      .then(r => r.json())
      .then(d => {
        if (d.results && d.results.length > 0) setPhoto(d.results[0].urls.regular)
        setPhotoLoading(false)
      })
      .catch(() => setPhotoLoading(false))
  }, [data.property_type, data.features])

  const handleDownload = async () => {
    const canvas = await html2canvas(flyerRef.current, {
      scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#ffffff'
    })
    const link = document.createElement('a')
    link.download = 'property-flyer.png'
    link.href = canvas.toDataURL('image/png')
    link.click()
  }

  const featureList = data.features
    ? data.features.split(',').map(f => f.trim()).slice(0, 6)
    : []

  const shortDesc = output?.listing ? output.listing.slice(0, 120) + '...' : ''

  return (
    <div className="flyer-wrapper">
      <div className="flyer-heading">Property Flyer</div>
      {photoLoading ? (
        <div className="flyer-loading">
          <span className="loading-dot" /><span className="loading-dot" /><span className="loading-dot" />
          <p>Fetching property photo...</p>
        </div>
      ) : (
        <>
          <div className="flyer-card-v2" ref={flyerRef}>
            <div className="blob blob-top-left" />
            <div className="blob blob-bottom-left" />
            <div className="blob blob-right" />
            <div className="flyer-v2-top">
              <div className="flyer-v2-left">
                <div className="flyer-v2-brand">
                  <div className="flyer-v2-brand-icon">✦</div>
                  <div>
                    <div className="flyer-v2-brand-name">AIREME</div>
                    <div className="flyer-v2-brand-sub">Real Estate</div>
                  </div>
                </div>
                <div className="flyer-v2-headline">
                  {data.property_type || 'Premium Property'}<br />
                  <span className="flyer-v2-headline-accent">For Sale</span>
                </div>
                <div className="flyer-v2-desc">{shortDesc}</div>
              </div>
              <div className="flyer-v2-right">
                <div className="flyer-circle-wrap">
                  {photo ? (
                    <img src={photo} alt="property" className="flyer-circle-img" crossOrigin="anonymous" />
                  ) : (
                    <div className="flyer-circle-placeholder">🏠</div>
                  )}
                  <div className="flyer-price-badge">
                    <div className="flyer-price-badge-label">Asking Price</div>
                    <div className="flyer-price-badge-value">{data.price}</div>
                  </div>
                </div>
              </div>
            </div>
            <div className="flyer-v2-divider" />
            <div className="flyer-v2-bottom">
              <div className="flyer-v2-section">
                <div className="flyer-v2-section-title">About This Property</div>
                <div className="flyer-v2-section-text">
                  Located in <strong>{data.location}</strong>. Ideal for {data.target_buyer}.
                </div>
              </div>
              <div className="flyer-v2-section">
                <div className="flyer-v2-section-title">Key Features</div>
                <div className="flyer-features-grid">
                  {featureList.map((f, i) => (
                    <div key={i} className="flyer-feature-item">
                      <span className="flyer-feature-dot" />{f}
                    </div>
                  ))}
                </div>
              </div>
              <div className="flyer-v2-section">
                <div className="flyer-contact-bar">
                  <span className="flyer-contact-icon">📍</span>
                  <span>{data.location}</span>
                </div>
              </div>
            </div>
            <div className="flyer-v2-footer">
              <span>www.aireme.com</span>
              <span>AI Real Estate Marketing Engine</span>
            </div>
          </div>
          <button className="download-btn" onClick={handleDownload}>Download Flyer</button>
        </>
      )}
    </div>
  )
}