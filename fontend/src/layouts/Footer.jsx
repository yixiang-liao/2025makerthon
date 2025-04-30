import React from 'react'

const Footer = () => {
  const currentYear = new Date().getFullYear();
  return (
    <div className="footer">
      <div className='img-group'>
        <div className='footer-img'>
          <img src="https://makerthon.nkust.edu.tw/site/themes/default/cht/images/logo_f.svg" alt="logo" />
        </div>
        <div className='footer-img1'>
          <img src="https://www.nkust.edu.tw/var/file/0/1000/img/513/182513897.png" alt="logo" />
        </div>
        <div className='footer-img1'>
          <img src="https://maker.nkust.edu.tw/2025skill/assets/OIE_LOGO_%E5%B7%A5%E4%BD%9C%E5%8D%80%E5%9F%9F%201-D3wW23uP.png" alt="logo" />
        </div>
      </div>
      <div className='footer-text'>
        <p>Copyright © {currentYear} I-Hsiang,Liao. All rights reserved.</p>
      </div>
    </div>
  )
}

export default Footer
