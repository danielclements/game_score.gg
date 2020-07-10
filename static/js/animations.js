// Gsap Animations

gsap.from('.anim1', {opacity: 0, duration: 0.4, y: 200, stagger: 0.3, ease: "power4.out"})




// Animation for login in page 
gsap.from('.login_forum', {opacity: 0, y: 100, duration: 1})
gsap.from('#username', {opacity: 0, duration: 0.6, delay: 0.3, x: -56})
gsap.from('#Password', {opacity: 0, duration: 0.6, delay: 0.3, x: 56})