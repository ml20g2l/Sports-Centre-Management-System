!function() {
    // to create a moment object which indicate to current date and time  
    var today = moment();

    // to call calendar constructor (selector- css selector, events - array of objects)
    function Calendar(selector, events) {
      // to assign HTML element to the 'el' property of the new 'Calendar' object 
      this.el = document.querySelector(selector);
      // to set the 'events' propery of the new 'Calendar' object to the 'events' arg
      this.events = events;
      // to set 'current' property of the new 'Calendar' object to a moment object
      // representing the first day of the current month. 
      this.current = moment().date(1);
      // call draw method 
      this.draw();
      // asssign the Html element with the 'today' calss ( the current date on the calendar.)
      var current = document.querySelector('.today');

      if(current) {
        var self = this;
        window.setTimeout(function() {
          self.openDay(current);
        }, 500);
      }
    }
    // this will be called by this.draw() method above 
    Calendar.prototype.draw = function() {
      //Create Header
      this.drawHeader();
  
      //Draw Month
      this.drawMonth();
  
      this.drawLegend();
    }
  
    Calendar.prototype.drawHeader = function() {
      var self = this;
      if(!this.header) {
        //Create the header elements
        this.header = createElement('div', 'header');
        this.header.className = 'header';
  
        this.title = createElement('h1');
      
        var right = createElement('div', 'right');
        right.addEventListener('click', function() { self.nextMonth(); });
  
        var left = createElement('div', 'left');
        left.addEventListener('click', function() { self.prevMonth(); });
  
        //Append the Elements
        this.header.appendChild(this.title); 
        this.header.appendChild(right);
        this.header.appendChild(left);
        this.el.appendChild(this.header);
        
      }
  
      this.title.innerHTML = this.current.format('MMMM YYYY');
      
    }
  
    Calendar.prototype.drawMonth = function() {
      var self = this;
      
      this.events.forEach(function(ev) {
       ev.date = self.current.clone().date(Math.random() * (29 - 1) + 1);
      });
      
      // Add "swimming pool" event on every Friday
      for (var i = 0; i < 5; i++) {
        var monday = this.current.clone().startOf('month').add('weeks', i).day('Fri');
        var event = {
          date: monday,
          eventName: 'Swimming Pool Team Events',
          color: 'green'
        };
        this.events.push(event);
      }
      // Add "swimming pool" event on every Sunday
      for (var i = 0; i < 5; i++) {
        var monday = this.current.clone().startOf('month').add('weeks', i).day('Sun');
        var event = {
          date: monday,
          eventName: 'Swimming Pool Team Events',
          color: 'green'
        };
        this.events.push(event);
      }
      // Add "Sports Hall" event on every Thursday
      for (var i = 0; i < 5; i++) {
        var monday = this.current.clone().startOf('month').add('weeks', i).day('Thu');
        var event = {
          date: monday,
          eventName: 'Sports Hall Team Events',
          color: 'blue'
        };
        this.events.push(event);
      }
      // Add "Sports Hall" event on every Saturday
      for (var i = 0; i < 5; i++) {
        var monday = this.current.clone().startOf('month').add('weeks', i).day('Sat');
        var event = {
          date: monday,
          eventName: 'Sports Hall Team Events',
          color: 'blue'
        };
        this.events.push(event);
      }
      // Add "Pilates" event every Monday
      for (var i = 0; i < 5; i++) {
        var wednesday = this.current.clone().startOf('month').add('weeks', i).day('Mon');
        var event = {
          date: wednesday,
          eventName: 'Pilates',
          color: 'orange'
        };
        this.events.push(event);
      }
      // Add "aerobics" event every Tuesday
      for (var i = 0; i < 5; i++) {
        var thursday = this.current.clone().startOf('month').add('weeks', i).day('Tue');
        var event = {
          date: thursday,
          eventName: 'Aerobics',
          color: 'yellow'
        };
        this.events.push(event);
      }
      // Add "Aerobics" event every Thursday
      for (var i = 0; i < 5; i++) {
        var thursday = this.current.clone().startOf('month').add('weeks', i).day('Thu');
        var event = {
          date: thursday,
          eventName: 'Aerobics',
          color: 'yellow'
        };
        this.events.push(event);
      }
      // Add "Aerobics" event every Saturday
      for (var i = 0; i < 5; i++) {
        var thursday = this.current.clone().startOf('month').add('weeks', i).day('Sat');
        var event = {
          date: thursday,
          eventName: 'Aerobics',
          color: 'yellow'
        };
        this.events.push(event);
      }
      // Add "yoga" event every Friday
      for (var i = 0; i < 5; i++) {
        var thursday = this.current.clone().startOf('month').add('weeks', i).day('Fri');
        var event = {
          date: thursday,
          eventName: 'Yoga',
          color: 'pink'
        };
        this.events.push(event);
      }
      // Add "Yoga" event every Sunday
      for (var i = 0; i < 5; i++) {
        var thursday = this.current.clone().startOf('month').add('weeks', i).day('Sunday');
        var event = {
          date: thursday,
          eventName: 'Yoga',
          color: 'pink'
        };
        this.events.push(event);


      }

      if(this.month) {
        this.oldMonth = this.month;
        this.oldMonth.className = 'month out ' + (self.next ? 'next' : 'prev');
        this.oldMonth.addEventListener('webkitAnimationEnd', function() {
          self.oldMonth.parentNode.removeChild(self.oldMonth);
          self.month = createElement('div', 'month');
          self.backFill();
          self.currentMonth();
          self.fowardFill();
          self.el.appendChild(self.month);
          window.setTimeout(function() {
            self.month.className = 'month in ' + (self.next ? 'next' : 'prev');
          }, 16);
        });
      } else {
          this.month = createElement('div', 'month');
          this.el.appendChild(this.month);
          this.backFill();
          this.currentMonth();
          this.fowardFill();
          this.month.className = 'month new';
      }
    }
  
    Calendar.prototype.backFill = function() {
      var clone = this.current.clone();
      var dayOfWeek = clone.day();
  
      if(!dayOfWeek) { return; }
  
      clone.subtract('days', dayOfWeek+1);
  
      for(var i = dayOfWeek; i > 0 ; i--) {
        this.drawDay(clone.add('days', 1));
      }
    }
  
    Calendar.prototype.fowardFill = function() {
      var clone = this.current.clone().add('months', 1).subtract('days', 1);
      var dayOfWeek = clone.day();
  
  
  
      if(dayOfWeek === 6) { return; }
  
      for(var i = dayOfWeek; i < 6 ; i++) {
        this.drawDay(clone.add('days', 1));
      }
    }
  
    Calendar.prototype.currentMonth = function() {
      var clone = this.current.clone();
  
      while(clone.month() === this.current.month()) {
        this.drawDay(clone);
        clone.add('days', 1);
      }
    }
  
    Calendar.prototype.getWeek = function(day) {
      if(!this.week || day.day() === 0) {
        this.week = createElement('div', 'week');
        this.month.appendChild(this.week);
      }
    }
    // ================= Modified part for implementing interactive calendar ======== 
    Calendar.prototype.drawDay = function(day) {
      var self = this;
      this.getWeek(day);
    
      //Outer Day
      var outer = createElement('div', this.getDayClass(day));
    
      outer.addEventListener('click', function() {
        self.openDay(this);
        // Styling: to change class name from center to col
        const calender = document.getElementsByClassName("center");
        if (calender.length > 0) {
          calender[0].setAttribute("class", "col");
        }    
        const card = document.getElementsByClassName("card")[0];
        card.style.left = "70%"; // Move card to the right further more
    
        var dateElement = this.querySelector('.day-number');
        if (dateElement) {
          var date = dateElement.innerText;
    
          // console.log("day name:" + this.querySelector('.day-name').textContent); 
    
          const dateString = self.title.innerHTML + ' ' + date;
          const date_object = new Date(dateString + " UTC"); // create a Date object with timezone set to UTC
          const isoDateString = date_object.toISOString().substring(0, 10); // format the date as an input date string
    
          const clickedDate = new Date(isoDateString); // create a Date object for the clicked date
          
          const eventList = document.getElementById('event-list');
          eventList.innerHTML = '';
          
          for (let i = 0; i < self.events.length; i++) {
            const eventDate = new Date(self.events[i].date); // create a Date object for the event date
                        
            // Compare the event date and clicked date
            if (eventDate.getFullYear() === clickedDate.getFullYear() &&
                eventDate.getMonth() === clickedDate.getMonth() &&
                eventDate.getDate() === clickedDate.getDate()) {
              // Create a new option for each event item
              const eventOption = document.createElement('option');
              eventOption.value = i;
              eventOption.textContent = self.events[i].eventName;

              // Append the option to the event list div
              eventList.appendChild(eventOption);

              
            }
          }
 
    
          // console.log("day:" + isoDateString); 
          document.querySelector('#date').innerHTML = isoDateString;
          var dayInput = document.querySelector('#day');
          dayInput.value = self.title.innerHTML + ' ' + date;
        }
      });
    
      //Day Name
      var name = createElement('div', 'day-name', day.format('ddd'));
    
      //Day Number
      var number = createElement('div', 'day-number', day.format('DD'));
    
      //Events
      var events = createElement('div', 'day-events');
      this.drawEvents(day, events);
    
      outer.appendChild(name);
      outer.appendChild(number);
      outer.appendChild(events);
      this.week.appendChild(outer);
    }
    // ============================================================== 


    Calendar.prototype.drawEvents = function(day, element) {
      if(day.month() === this.current.month()) {
        var todaysEvents = this.events.reduce(function(memo, ev) {
          if(ev.date.isSame(day, 'day')) {
            memo.push(ev);
          }
          return memo;
        }, []);
  
        todaysEvents.forEach(function(ev) {
          var evSpan = createElement('span', ev.color);
          element.appendChild(evSpan);
        });
      }
    }
  
    Calendar.prototype.getDayClass = function(day) {
      classes = ['day'];
      if(day.month() !== this.current.month()) {
        classes.push('other');
      } else if (today.isSame(day, 'day')) {
        classes.push('today');
      }
      return classes.join(' ');
    }
  
    Calendar.prototype.openDay = function(el) {
      var details, arrow;
      var dayNumber = +el.querySelectorAll('.day-number')[0].innerText || +el.querySelectorAll('.day-number')[0].textContent;
      var day = this.current.clone().date(dayNumber);

  
      var currentOpened = document.querySelector('.details');
  
      //Check to see if there is an open detais box on the current row
      if(currentOpened && currentOpened.parentNode === el.parentNode) {
        details = currentOpened;
        arrow = document.querySelector('.arrow');
      } else {
        //Close the open events on differnt week row
        //currentOpened && currentOpened.parentNode.removeChild(currentOpened);
        if(currentOpened) {
          currentOpened.addEventListener('webkitAnimationEnd', function() {
            currentOpened.parentNode.removeChild(currentOpened);
          });
          currentOpened.addEventListener('oanimationend', function() {
            currentOpened.parentNode.removeChild(currentOpened);
          });
          currentOpened.addEventListener('msAnimationEnd', function() {
            currentOpened.parentNode.removeChild(currentOpened);
          });
          currentOpened.addEventListener('animationend', function() {
            currentOpened.parentNode.removeChild(currentOpened);
          });
          currentOpened.className = 'details out';
        }
  
        //Create the Details Container
        details = createElement('div', 'details in');
  
        //Create the arrow
        var arrow = createElement('div', 'arrow');
  
        //Create the event wrapper
  
        details.appendChild(arrow);
        el.parentNode.appendChild(details);
      }
  
      var todaysEvents = this.events.reduce(function(memo, ev) {
        if(ev.date.isSame(day, 'day')) {
          memo.push(ev);
        }
        return memo;
      }, []);
  
      this.renderEvents(todaysEvents, details);
  
      arrow.style.left = el.offsetLeft - el.parentNode.offsetLeft + 27 + 'px';
    }
  
    Calendar.prototype.renderEvents = function(events, ele) {
      //Remove any events in the current details element
      var currentWrapper = ele.querySelector('.events');
      var wrapper = createElement('div', 'events in' + (currentWrapper ? ' new' : ''));
  
      events.forEach(function(ev) {
        var div = createElement('div', 'event');
        var square = createElement('div', 'event-category ' + ev.color);
        var span = createElement('span', '', ev.eventName);
  
        div.appendChild(square);
        div.appendChild(span);
        wrapper.appendChild(div);
      });
  
      if(!events.length) {
        var div = createElement('div', 'event empty');
        var span = createElement('span', '', 'No Events');
  
        div.appendChild(span);
        wrapper.appendChild(div);
      }
  
      if(currentWrapper) {
        currentWrapper.className = 'events out';
        currentWrapper.addEventListener('webkitAnimationEnd', function() {
          currentWrapper.parentNode.removeChild(currentWrapper);
          ele.appendChild(wrapper);
        });
        currentWrapper.addEventListener('oanimationend', function() {
          currentWrapper.parentNode.removeChild(currentWrapper);
          ele.appendChild(wrapper);
        });
        currentWrapper.addEventListener('msAnimationEnd', function() {
          currentWrapper.parentNode.removeChild(currentWrapper);
          ele.appendChild(wrapper);
        });
        currentWrapper.addEventListener('animationend', function() {
          currentWrapper.parentNode.removeChild(currentWrapper);
          ele.appendChild(wrapper);
        });
      } else {
        ele.appendChild(wrapper);
      }
    }
  
    Calendar.prototype.drawLegend = function() {
      var legend = createElement('div', 'legend');
      var calendars = this.events.map(function(e) {
        return e.calendar + '|' + e.color;
      }).reduce(function(memo, e) {
        if(memo.indexOf(e) === -1) {
          memo.push(e);
        }
        return memo;
      }, []).forEach(function(e) {
        var parts = e.split('|');
        var entry = createElement('span', 'entry ' +  parts[1], parts[0]);
        legend.appendChild(entry);
      });
      this.el.appendChild(legend);
    }
  
    Calendar.prototype.nextMonth = function() {
      if (this.current.month() === 11) {
        this.current = moment({year: this.current.year() + 1, month: 0, day: 1});
      } else {
        this.current = moment({year: this.current.year(), month: this.current.month() + 1, day: 1});
      }
      this.events = this.filterEventsByMonth(this.events);
      this.draw();
    }
    
    Calendar.prototype.prevMonth = function() {
      if (this.current.month() === 0) {
        this.current = moment({year: this.current.year() - 1, month: 11, day: 1});
      } else {
        this.current = moment({year: this.current.year(), month: this.current.month() - 1, day: 1});
      }
      this.events = this.filterEventsByMonth(this.events);
      this.draw();
    }
    
    Calendar.prototype.filterEventsByMonth = function(events) {
      var self = this;
      return events.filter(function(ev) {
        return ev.date.month() === self.current.month();
      });
    }
    
  
    window.Calendar = Calendar;
  
    function createElement(tagName, className, innerText) {
      var ele = document.createElement(tagName);
      if(className) {
        ele.className = className;
      }
      if(innerText) {
        ele.innderText = ele.textContent = innerText;
      }
      return ele;
    }
    
  }();
  
  !function() {
    var data = [];
    function addDate(ev) {}
    var calendar = new Calendar('#calendar', data);
  }();


// Slider Revolution. (n.d.). HTML Calendar. Retrieved December 1, 2021, from https://www.sliderrevolution.com/resources/html-calendar/


