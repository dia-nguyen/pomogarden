const cursor = document.querySelector('.cursor');
const plots = document.querySelectorAll('.plot')
const sowed = document.querySelectorAll('.sowed')
const planted = document.querySelectorAll('.planted')
const watered = document.querySelectorAll('.watered')
const readyToSell = document.querySelectorAll('.ready-to-sell')

plots.forEach(plot => {
  plot.addEventListener('mouseenter', e => {
    cursor.classList.add('hoe')
  })
  plot.addEventListener('mouseleave', e => {
    cursor.classList.remove('hoe')
  })
})

sowed.forEach(plot => {
  plot.addEventListener('mouseenter', e => {
    cursor.classList.add('seeds')
  })
  plot.addEventListener('mouseleave', e => {
    cursor.classList.remove('seeds')
  })
})

planted.forEach(plot => {
  plot.addEventListener('mouseenter', e => {
    cursor.classList.add('watercan')
  })
  plot.addEventListener('mouseleave', e => {
    cursor.classList.remove('watercan')
  })
})

watered.forEach(plot => {
  plot.addEventListener('mouseenter', e => {
    cursor.classList.add('no-thanks')
  })
  plot.addEventListener('mouseleave', e => {
    cursor.classList.remove('no-thanks')
  })
})

readyToSell.forEach(plot => {
  plot.addEventListener('mouseenter', e => {
    cursor.classList.add('sell')
  })
  plot.addEventListener('mouseleave', e => {
    cursor.classList.remove('sell')
  })
})

document.addEventListener('mousemove', e => {
  cursor.setAttribute("style", "top: " + e.pageY + "px; left: " + e.pageX + "px;")
})