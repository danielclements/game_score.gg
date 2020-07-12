// Gsap Animations

gsap.from('.anim1', {opacity: 0, duration: 1, y: 200, stagger: 0.3, ease: "power4.out"})




// Animation for login in page 
gsap.from('.login_forum', {opacity: 0, y: 100, duration: 1})
gsap.from('#username', {opacity: 0, duration: 0.7, delay: 0.3, x: -56})
gsap.from('#Password', {opacity: 0, duration: 0.7, delay: 0.3, x: 56})


// Animations for the home page

gsap.from('.game-details-p', {opacity: 0, x: 100, duration: 1, stagger: 0.2})
gsap.from('.recent_games', {opacity: 0, duration: 1.2, stagger: 0.3, x: -150})
gsap.from('.recent_devs', {opacity: 0, duration: 1.2, stagger: 0.3, y: -150})
gsap.from('.recent_pubs', {opacity: 0, duration: 1.2, stagger: 0.3, x: 150})

// Animations for review page
gsap.from('#game_summary', {opacity: 0, duration: 1.3, x: -100, ease: "slow(0.7, 0.7, false)"})
gsap.from('.review-img', {opacity: 0, duration: 1.6, x: -150, ease: "sine.out"})
