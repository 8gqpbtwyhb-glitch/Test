# -*- coding: utf-8 -*-
"""All the words, facts and photo choices of the Allofts website.

Edit this file to change a price, a phone number, a sentence or a photo,
then run:  python3 build.py
Photo paths are relative to the ../photos folder.
"""

LANGS = ["en", "el"]

SITE = {
    "name": "Allofts",
    "url": "https://allofts.gr",          # public address, used for search-engine tags
    "email": "info@allofts.gr",
    "phones": [                           # (dial string, shown as)
        ("+302721097553", "+30 27210 97553"),
        ("+306976299678", "+30 697 629 9678"),
        ("+306986524901", "+30 698 652 4901"),
    ],
    "address": {
        "en": ["Avras 9", "Kalamata 24100, Greece"],
        "el": ["Αύρας 9", "Καλαμάτα 24100"],
    },
    "maps_link": "https://www.google.com/maps/search/?api=1&query=%CE%91%CF%8D%CF%81%CE%B1%CF%82+9%2C+%CE%9A%CE%B1%CE%BB%CE%B1%CE%BC%CE%AC%CF%84%CE%B1+24100",
    "maps_embed": "https://maps.google.com/maps?q=%CE%91%CF%8D%CF%81%CE%B1%CF%82%209%2C%20%CE%9A%CE%B1%CE%BB%CE%B1%CE%BC%CE%AC%CF%84%CE%B1&t=m&z=15&output=embed&iwloc=near",
    "booking": {
        "en": "https://www.booking.com/hotel/gr/allofts.html",
        "el": "https://www.booking.com/hotel/gr/allofts.el.html",
    },
    "facebook": "https://www.facebook.com/profile.php?id=61550821376523",
    "instagram": "https://www.instagram.com/allofts_apartments/",
    "price_from": 130,                    # euros per night, shown as "from"
}

# ----------------------------------------------------------------------------
# Interface text
# ----------------------------------------------------------------------------
T = {
    "en": {
        "lang_name": "English", "lang_short": "EN", "other_short": "ΕΛ", "other_name": "Ελληνικά",
        "skip": "Skip to content",
        "nav_rooms": "Lofts & Suites", "nav_house": "The House", "nav_gallery": "Gallery", "nav_contact": "Contact",
        "nav_home": "Home",
        "book": "Book now", "book_short": "Book", "enquire": "Send an enquiry", "call": "Call",
        "menu": "Menu", "close": "Close",
        "tagline": "Contemporary Living",
        "motto": "Your place. To stay, to live, to inspire, to be.",

        # home — hero
        "hero_eyebrow": "Contemporary living · Kalamata, Greece",
        "hero_title": "Your place.<br>To stay, to live,<br><em>to inspire</em>, to be.",
        "hero_lede": "Eight design-led lofts and suites with a roof garden above the city, close to the sea. Feel like home.",
        "hero_cta": "Explore the lofts",
        "hero_house": "The house",
        "slide": "Slide",

        # home — welcome
        "welcome_eyebrow": "Welcome to Allofts",
        "welcome_title": "A house of eight lofts and suites, each with a character of its own.",
        "welcome_p": "Nestled in the beautiful city of Kalamata, our apartments combine timeless elegance with modern comfort to give you a truly exceptional stay. From the moment you step through our doors, you’ll be enveloped in an atmosphere of refined urban luxury and impeccable hospitality.",
        "welcome_link": "About the house",
        "welcome_caption": "Avras 9, Kalamata",
        "stat_1": ("8", "Lofts & suites"),
        "stat_2": ("28–56 m²", "Of private space"),
        "stat_3": ("2–4", "Guests per stay"),
        "stat_4": ("1", "Roof garden above the city"),

        # home — rooms
        "rooms_eyebrow": "Stay",
        "rooms_title": "The lofts & suites",
        "rooms_intro": "Allofts offers a range of meticulously designed lofts, suites and rooms, each exuding its own distinct charm and character.",
        "rooms_all": "View all lofts & suites",
        "view": "View", "discover": "Discover",
        "prev": "Previous", "next": "Next",

        "marquee": ["to stay", "to live", "to inspire", "to be"],

        # home — house
        "house_eyebrow": "The house",
        "roof_title": "Above it all, a roof garden",
        "roof_p": "A timber deck, a long table and deep loungers under the open sky, with the city below and the mountains beyond. Come up for a coffee in the morning light, or a glass of wine as the sun goes down.",
        "gym_title": "And a gym in the house",
        "gym_p": "Keep your routine while you travel: an in-house fitness room with a treadmill, spin bikes and a multi-gym station.",
        "house_link": "More about the house",

        # home — amenities
        "amen_eyebrow": "Comfort",
        "amen_title": "In every stay",
        "amen_p": "Whichever loft or suite you choose, the essentials are taken care of.",

        # home — gallery teaser
        "gal_eyebrow": "Gallery",
        "gal_title": "A closer look",
        "gal_link": "Open the gallery",

        # home — guests
        "guests_eyebrow": "Guests",
        "guests_title": "Kind words",
        "translated": "Translated from Greek",

        # location
        "loc_eyebrow": "Location",
        "loc_title": "Avras 9, Kalamata",
        "loc_p": "A residential neighbourhood of Kalamata, close to the beach — an easy base for the city, the seafront and the rest of Messinia.",
        "loc_maps": "Open in Google Maps",
        "loc_load": "Show the map",
        "loc_note": "The map is provided by Google and loads only when you ask for it.",
        "loc_here": "Allofts",

        # call to action
        "cta_title": "Ready when you are.",
        "cta_p": "Book online or get in touch — the reservations team is at your disposal.",

        # footer
        "f_visit": "Visit", "f_call": "Call & write", "f_explore": "Explore", "f_follow": "Follow",
        "f_rights": "All rights reserved.", "f_privacy": "Privacy",
        "f_top": "Back to top",

        # rooms index
        "rooms_page_title": "Lofts & Suites",
        "rooms_page_lede": "Whether you’re seeking a tranquil retreat for a romantic getaway or a spacious haven for a family holiday, our accommodations offer the perfect blend of style and functionality.",
        "rooms_meta_title": "Lofts & Suites in Kalamata",
        "rooms_meta_desc": "Eight design-led lofts, suites and rooms from 28 to 56 m² at Allofts, Kalamata. Compare them and choose your place to stay.",

        # room page
        "kind": {"loft": "Loft", "suite": "Suite", "apartment": "Apartment", "room": "Room"},
        "size": "Size", "guests": "Guests", "bed": "Bed", "from": "From", "night": "night",
        "sqm": "m²", "upto": "Up to {n} guests", "upto_short": "Up to {n}",
        "bed_queen": "Queen-size bed", "bed_queen_short": "Queen-size",
        "sofa_1": "Sofa bed for 1 extra guest", "sofa_2": "Sofa bed for 2 extra guests",
        "about_room": "About this space",
        "facilities": "Facilities",
        "photos": "Photos", "all_photos": "View all {n} photos",
        "more_photos": "More of {name}",
        "book_title": "Stay here",
        "book_booking": "Book on Booking.com",
        "book_ask": "Ask about this {kind}",
        "book_note": "Prices vary with dates and length of stay. For the best direct offer, call or write to us.",
        "next_room": "Next", "prev_room": "Previous", "all_rooms": "All lofts & suites",
        "price_from": "From €{p}", "per_night": "/ night", "in_city": "in Kalamata",

        # gallery page
        "gallery_page_title": "Gallery",
        "gallery_page_lede": "The lofts, the house and the roof garden, in pictures.",
        "gallery_meta_desc": "Photo gallery of Allofts in Kalamata: the lofts and suites, the building and the roof garden.",
        "f_all": "All", "f_lofts": "Lofts & suites", "f_house": "The house", "f_roof": "Roof garden & gym",

        # about page
        "about_meta_title": "The House",
        "about_meta_desc": "The story of Allofts: eight lofts and suites, a roof garden and a gym in Kalamata. Your place to stay, to live, to inspire, to be.",
        "about_eyebrow": "The house",
        "about_title": "Your place. To stay, to live, to inspire, to be.",
        "about_ps": [
            "Nestled in the beautiful city of Kalamata, our apartments combine timeless elegance with modern comfort to provide you with a truly exceptional stay. From the moment you step through our doors, you’ll be enveloped in an atmosphere of refined urban luxury and impeccable hospitality.",
            "Allofts offers a range of meticulously designed lofts and suites, each exuding its own distinct charm and character.",
            "Whether you’re seeking a tranquil retreat for a romantic getaway or a spacious haven for a family holiday, our accommodations offer the perfect blend of style and functionality. With our attention to detail, we strive to provide a space you’ll be proud to call home.",
            "We look forward to welcoming you to Allofts and ensuring your stay with us is nothing short of extraordinary. Let us be your home away from home, where luxury meets hospitality in perfect harmony.",
        ],
        "verbs_title": "Four ways to feel at home",
        "verbs": [
            ("To stay", "Eight lofts, suites and rooms from 28 to 56 m², each designed down to the last detail."),
            ("To live", "Equipped kitchens, living areas and room to settle in — for a weekend or for longer."),
            ("To inspire", "A mural, a suspended net, a crystal chandelier, hand-picked furniture: no two spaces are alike."),
            ("To be", "A roof garden, a gym and hosts who are there whenever you need them."),
        ],
        "about_roof_eyebrow": "On the roof",
        "about_gym_eyebrow": "Fitness",
        "about_building_eyebrow": "The building",
        "about_building_title": "White volumes, concrete and light",
        "about_building_p": "Clean white volumes, exposed concrete and black steel by day; a soft play of light once the sun has set. A discreet entrance, a sculptural staircase and a lift lead to each door.",

        # contact page
        "contact_meta_title": "Contact & Reservations",
        "contact_meta_desc": "Contact Allofts in Kalamata: Avras 9, tel. +30 27210 97553, info@allofts.gr. Send an enquiry or book online.",
        "contact_eyebrow": "Contact",
        "contact_title": "Let’s plan your stay",
        "contact_p": "For any information, please do not hesitate to contact us. The reservations team will be at your disposal.",
        "c_address": "Address", "c_phones": "Phones", "c_email": "Email", "c_social": "Social",
        "form_title": "Send a message",
        "form_name": "Your name", "form_email": "Email", "form_phone": "Phone",
        "form_room": "Loft or suite", "form_any": "No preference",
        "form_in": "Check-in", "form_out": "Check-out", "form_guests": "Guests",
        "form_msg": "Message", "form_msg_ph": "Tell us about your stay…",
        "form_send": "Send enquiry",
        "form_hint": "This opens your email app with the message ready to send — nothing is stored on this website.",
        "form_done": "Your email app should now be open with the message ready. If nothing happened, write to us at info@allofts.gr or give us a call.",
        "form_subject": "Stay enquiry",
        "form_required": "Please fill in your name and email.",
        "mail_labels": {"name": "Name", "email": "Email", "phone": "Phone", "room": "Preference", "in": "Check-in", "out": "Check-out", "guests": "Guests", "msg": "Message"},

        # privacy
        "privacy_title": "Privacy",
        "privacy_meta_desc": "How the Allofts website treats your privacy: no cookies, no tracking.",
        "privacy_intro": "This website is a simple brochure for Allofts, built to respect your privacy.",
        "privacy_items": [
            ("No cookies, no tracking", "We do not use cookies, analytics or advertising trackers on this website. Fonts and images are served by the website itself, not by third parties."),
            ("Enquiry form", "The form on the Contact page does not send anything through the website. It prepares an email in your own email app, and nothing is sent until you press send there. When you email or call us, we use your details only to answer your request and to manage your reservation."),
            ("Map", "The map is provided by Google and loads only when you ask for it. From that moment, Google’s own privacy policy applies."),
            ("Booking", "When you choose “Book now” you leave this website for Booking.com, where their terms and privacy policy apply."),
            ("Questions", "For anything concerning your personal data, write to us at info@allofts.gr."),
        ],

        # 404
        "nf_title": "This page has checked out.",
        "nf_p": "The page you are looking for does not exist or has moved.",
        "nf_home": "Back to the home page",

        "moved": "This page has moved.",

        # photo labels (alt text and captions)
        "tags": {
            "living": "Living area", "bedroom": "Bedroom", "kitchen": "Kitchen", "dining": "Dining area",
            "bathroom": "Bathroom", "terrace": "Terrace", "balcony": "Balcony", "garden": "Garden",
            "stairs": "Staircase", "detail": "Detail", "net": "Relaxation net", "view": "Interior view",
            "exterior": "The building", "entrance": "Entrance", "lobby": "Common areas", "roof": "Roof garden",
            "gym": "Gym", "aerial": "Aerial view",
        },
        "home_meta_title": "Allofts — Contemporary lofts & suites in Kalamata, Greece",
        "home_meta_desc": "Allofts: eight design-led lofts and suites in Kalamata with a roof garden and gym, close to the sea. Your place to stay, to live, to inspire, to be.",
    },

    "el": {
        "lang_name": "Ελληνικά", "lang_short": "ΕΛ", "other_short": "EN", "other_name": "English",
        "skip": "Μετάβαση στο περιεχόμενο",
        "nav_rooms": "Lofts & Σουίτες", "nav_house": "Ο Χώρος", "nav_gallery": "Gallery", "nav_contact": "Επικοινωνία",
        "nav_home": "Αρχική",
        "book": "Κάντε κράτηση", "book_short": "Κράτηση", "enquire": "Στείλτε μήνυμα", "call": "Κλήση",
        "menu": "Μενού", "close": "Κλείσιμο",
        "tagline": "Contemporary Living",
        "motto": "Ο χώρος σας. Για να μείνετε, να ζήσετε, να εμπνευστείτε.",

        "hero_eyebrow": "Contemporary living · Καλαμάτα",
        "hero_title": "Ο χώρος σας.<br>Για να μείνετε,<br class=\"br-m\"> να ζήσετε,<br><em>να εμπνευστείτε</em>.",
        "hero_lede": "Οκτώ lofts και σουίτες με ξεχωριστό χαρακτήρα και ένα roof garden πάνω από την πόλη, κοντά στη θάλασσα. Αισθανθείτε σαν στο σπίτι σας.",
        "hero_cta": "Δείτε τα lofts",
        "hero_house": "Ο χώρος",
        "slide": "Εικόνα",

        "welcome_eyebrow": "Καλώς ορίσατε στο Allofts",
        "welcome_title": "Ένα σπίτι με οκτώ lofts και σουίτες, το καθένα με τον δικό του χαρακτήρα.",
        "welcome_p": "Στην όμορφη πόλη της Καλαμάτας, τα διαμερίσματά μας συνδυάζουν τη διαχρονική κομψότητα με τη σύγχρονη άνεση για να σας προσφέρουν μια πραγματικά εξαιρετική διαμονή. Από τη στιγμή που θα περάσετε την πόρτα μας, θα αισθανθείτε μια ατμόσφαιρα πολυτέλειας και αψεγάδιαστης φιλοξενίας.",
        "welcome_link": "Γνωρίστε τον χώρο",
        "welcome_caption": "Αύρας 9, Καλαμάτα",
        "stat_1": ("8", "Lofts & σουίτες"),
        "stat_2": ("28–56 τ.μ.", "Ιδιωτικού χώρου"),
        "stat_3": ("2–4", "Άτομα ανά διαμονή"),
        "stat_4": ("1", "Roof garden πάνω από την πόλη"),

        "rooms_eyebrow": "Διαμονή",
        "rooms_title": "Τα lofts & οι σουίτες",
        "rooms_intro": "Το Allofts διαθέτει μια σειρά από lofts, σουίτες και δωμάτια, προσεκτικά σχεδιασμένα το καθένα, με τη δική του ξεχωριστή γοητεία και χαρακτήρα.",
        "rooms_all": "Δείτε όλα τα lofts & τις σουίτες",
        "view": "Δείτε", "discover": "Ανακαλύψτε",
        "prev": "Προηγούμενο", "next": "Επόμενο",

        "marquee": ["να μείνετε", "να ζήσετε", "να εμπνευστείτε", "σαν στο σπίτι σας"],

        "house_eyebrow": "Ο χώρος",
        "roof_title": "Πάνω απ’ όλα, ένα roof garden",
        "roof_p": "Ξύλινο deck, ένα μεγάλο τραπέζι και αναπαυτικά πουφ κάτω από τον ανοιχτό ουρανό, με την πόλη στα πόδια σας και τα βουνά στον ορίζοντα. Ανεβείτε για έναν καφέ στο πρωινό φως ή για ένα ποτήρι κρασί την ώρα που δύει ο ήλιος.",
        "gym_title": "Και ένα γυμναστήριο στο κτίριο",
        "gym_p": "Κρατήστε τη ρουτίνα σας και στο ταξίδι: χώρος γυμναστικής μέσα στο κτίριο, με διάδρομο, ποδήλατα και πολυόργανο.",
        "house_link": "Περισσότερα για τον χώρο",

        "amen_eyebrow": "Άνεση",
        "amen_title": "Σε κάθε διαμονή",
        "amen_p": "Όποιο loft ή σουίτα κι αν επιλέξετε, τα βασικά είναι ήδη φροντισμένα.",

        "gal_eyebrow": "Gallery",
        "gal_title": "Μια πιο κοντινή ματιά",
        "gal_link": "Δείτε το gallery",

        "guests_eyebrow": "Επισκέπτες",
        "guests_title": "Είπαν για εμάς",
        "translated": "Μετάφραση από τα ελληνικά",

        "loc_eyebrow": "Τοποθεσία",
        "loc_title": "Αύρας 9, Καλαμάτα",
        "loc_p": "Σε μια γειτονιά της Καλαμάτας, κοντά στην παραλία — ιδανική βάση για την πόλη, το παραλιακό μέτωπο και όλη τη Μεσσηνία.",
        "loc_maps": "Άνοιγμα στο Google Maps",
        "loc_load": "Εμφάνιση χάρτη",
        "loc_note": "Ο χάρτης παρέχεται από την Google και φορτώνει μόνο όταν το ζητήσετε.",
        "loc_here": "Allofts",

        "cta_title": "Σας περιμένουμε.",
        "cta_p": "Κάντε κράτηση online ή επικοινωνήστε μαζί μας — το τμήμα κρατήσεων είναι στη διάθεσή σας.",

        "f_visit": "Διεύθυνση", "f_call": "Επικοινωνία", "f_explore": "Εξερευνήστε", "f_follow": "Ακολουθήστε μας",
        "f_rights": "Με επιφύλαξη παντός δικαιώματος.", "f_privacy": "Απόρρητο",
        "f_top": "Επιστροφή επάνω",

        "rooms_page_title": "Lofts & Σουίτες",
        "rooms_page_lede": "Είτε ψάχνετε ένα ήσυχο καταφύγιο για μια ρομαντική απόδραση είτε έναν ευρύχωρο χώρο για οικογενειακές διακοπές, τα διαμερίσματά μας προσφέρουν τον ιδανικό συνδυασμό στυλ και λειτουργικότητας.",
        "rooms_meta_title": "Lofts & Σουίτες στην Καλαμάτα",
        "rooms_meta_desc": "Οκτώ lofts, σουίτες και δωμάτια από 28 έως 56 τ.μ. στο Allofts, στην Καλαμάτα. Συγκρίνετε και επιλέξτε τον χώρο σας.",

        "kind": {"loft": "Loft", "suite": "Σουίτα", "apartment": "Διαμέρισμα", "room": "Δωμάτιο"},
        "size": "Μέγεθος", "guests": "Άτομα", "bed": "Κρεβάτι", "from": "Από", "night": "νύχτα",
        "sqm": "τ.μ.", "upto": "Έως {n} άτομα", "upto_short": "Έως {n}",
        "bed_queen": "Κρεβάτι queen size", "bed_queen_short": "Queen size",
        "sofa_1": "Καναπές-κρεβάτι για 1 επιπλέον άτομο", "sofa_2": "Καναπές-κρεβάτι για 2 επιπλέον άτομα",
        "about_room": "Περιγραφή",
        "facilities": "Παροχές",
        "photos": "Φωτογραφίες", "all_photos": "Δείτε και τις {n} φωτογραφίες",
        "more_photos": "Περισσότερα από το {name}",
        "book_title": "Μείνετε εδώ",
        "book_booking": "Κράτηση στο Booking.com",
        "book_ask": "Ρωτήστε μας γι’ αυτόν τον χώρο",
        "book_note": "Οι τιμές διαφέρουν ανάλογα με τις ημερομηνίες και τη διάρκεια διαμονής. Για την καλύτερη προσφορά, καλέστε ή γράψτε μας.",
        "next_room": "Επόμενο", "prev_room": "Προηγούμενο", "all_rooms": "Όλα τα lofts & οι σουίτες",
        "price_from": "Από €{p}", "per_night": "/ νύχτα", "in_city": "στην Καλαμάτα",

        "gallery_page_title": "Gallery",
        "gallery_page_lede": "Τα lofts, το κτίριο και το roof garden, σε εικόνες.",
        "gallery_meta_desc": "Φωτογραφίες του Allofts στην Καλαμάτα: τα lofts και οι σουίτες, το κτίριο και το roof garden.",
        "f_all": "Όλα", "f_lofts": "Lofts & σουίτες", "f_house": "Το κτίριο", "f_roof": "Roof garden & γυμναστήριο",

        "about_meta_title": "Ο Χώρος",
        "about_meta_desc": "Η ιστορία του Allofts: οκτώ lofts και σουίτες, roof garden και γυμναστήριο στην Καλαμάτα. Ο χώρος σας, για να μείνετε, να ζήσετε, να εμπνευστείτε.",
        "about_eyebrow": "Ο χώρος",
        "about_title": "Ο χώρος σας. Για να μείνετε, να ζήσετε, να εμπνευστείτε.",
        "about_ps": [
            "Στην όμορφη πόλη της Καλαμάτας, τα διαμερίσματά μας συνδυάζουν τη διαχρονική κομψότητα με τη σύγχρονη άνεση για να σας προσφέρουν μια πραγματικά εξαιρετική διαμονή. Από τη στιγμή που θα περάσετε την πόρτα μας, θα αισθανθείτε μια ατμόσφαιρα πολυτέλειας και αψεγάδιαστης φιλοξενίας.",
            "Το Allofts διαθέτει μια σειρά από διαμερίσματα και σουίτες, προσεκτικά σχεδιασμένα το καθένα, με τη δική του ξεχωριστή γοητεία και χαρακτήρα.",
            "Είτε ψάχνετε ένα ήσυχο καταφύγιο για μια ρομαντική απόδραση είτε έναν ευρύχωρο χώρο για οικογενειακές διακοπές, τα διαμερίσματά μας προσφέρουν τον ιδανικό, μοντέρνο και αστικό συνδυασμό στυλ και λειτουργικότητας. Δίνοντας έμφαση στη λεπτομέρεια, προσπαθούμε να σας προσφέρουμε έναν χώρο που θα μπορείτε να αποκαλείτε σπίτι.",
            "Ανυπομονούμε να σας καλωσορίσουμε στο Allofts και να φροντίσουμε ώστε η διαμονή σας να είναι εξαιρετική. Ας γίνουμε το σπίτι σας μακριά από το σπίτι, εκεί όπου η πολυτέλεια και η άνεση συναντούν τη φιλοξενία.",
        ],
        "verbs_title": "Τέσσερις τρόποι να νιώσετε σαν στο σπίτι σας",
        "verbs": [
            ("Να μείνετε", "Οκτώ lofts, σουίτες και δωμάτια από 28 έως 56 τ.μ., σχεδιασμένα μέχρι την τελευταία λεπτομέρεια."),
            ("Να ζήσετε", "Εξοπλισμένες κουζίνες, καθιστικά και χώρος για να νιώσετε άνετα — για ένα Σαββατοκύριακο ή για περισσότερο."),
            ("Να εμπνευστείτε", "Μια τοιχογραφία, ένα αιωρούμενο δίχτυ, ένας κρυστάλλινος πολυέλαιος, προσεκτικά διαλεγμένα έπιπλα: κανένας χώρος δεν μοιάζει με άλλον."),
            ("Να είστε ο εαυτός σας", "Ένα roof garden, ένα γυμναστήριο και οικοδεσπότες που είναι δίπλα σας όποτε τους χρειαστείτε."),
        ],
        "about_roof_eyebrow": "Στην ταράτσα",
        "about_gym_eyebrow": "Στο κτίριο",
        "about_building_eyebrow": "Το κτίριο",
        "about_building_title": "Λευκοί όγκοι, μπετόν και φως",
        "about_building_p": "Καθαροί λευκοί όγκοι, εμφανές μπετόν και μαύρο μέταλλο την ημέρα· ένα διακριτικό παιχνίδι φωτός μόλις δύσει ο ήλιος. Μια διακριτική είσοδος, μια γλυπτική σκάλα και ένας ανελκυστήρας οδηγούν σε κάθε πόρτα.",

        "contact_meta_title": "Επικοινωνία & Κρατήσεις",
        "contact_meta_desc": "Επικοινωνήστε με το Allofts στην Καλαμάτα: Αύρας 9, τηλ. 27210 97553, info@allofts.gr. Στείλτε μήνυμα ή κάντε κράτηση online.",
        "contact_eyebrow": "Επικοινωνία",
        "contact_title": "Ας οργανώσουμε τη διαμονή σας",
        "contact_p": "Για οποιαδήποτε πληροφορία, μη διστάσετε να επικοινωνήσετε μαζί μας. Το τμήμα κρατήσεων θα είναι στη διάθεσή σας.",
        "c_address": "Διεύθυνση", "c_phones": "Τηλέφωνα", "c_email": "Email", "c_social": "Social",
        "form_title": "Στείλτε μας μήνυμα",
        "form_name": "Ονοματεπώνυμο", "form_email": "Email", "form_phone": "Τηλέφωνο",
        "form_room": "Loft ή σουίτα", "form_any": "Χωρίς προτίμηση",
        "form_in": "Άφιξη", "form_out": "Αναχώρηση", "form_guests": "Άτομα",
        "form_msg": "Μήνυμα", "form_msg_ph": "Πείτε μας για τη διαμονή σας…",
        "form_send": "Αποστολή",
        "form_hint": "Θα ανοίξει η εφαρμογή email σας με το μήνυμα έτοιμο για αποστολή — τίποτα δεν αποθηκεύεται σε αυτόν τον ιστότοπο.",
        "form_done": "Η εφαρμογή email σας θα πρέπει να έχει ανοίξει με το μήνυμα έτοιμο. Αν δεν συνέβη κάτι, γράψτε μας στο info@allofts.gr ή καλέστε μας.",
        "form_subject": "Ερώτηση για διαμονή",
        "form_required": "Συμπληρώστε το όνομα και το email σας.",
        "mail_labels": {"name": "Όνομα", "email": "Email", "phone": "Τηλέφωνο", "room": "Προτίμηση", "in": "Άφιξη", "out": "Αναχώρηση", "guests": "Άτομα", "msg": "Μήνυμα"},

        "privacy_title": "Απόρρητο",
        "privacy_meta_desc": "Πώς ο ιστότοπος του Allofts σέβεται το απόρρητό σας: χωρίς cookies, χωρίς παρακολούθηση.",
        "privacy_intro": "Αυτός ο ιστότοπος είναι μια απλή παρουσίαση του Allofts, φτιαγμένη ώστε να σέβεται το απόρρητό σας.",
        "privacy_items": [
            ("Χωρίς cookies, χωρίς παρακολούθηση", "Δεν χρησιμοποιούμε cookies, εργαλεία στατιστικών ή διαφημιστικούς ιχνηλάτες. Οι γραμματοσειρές και οι εικόνες φορτώνονται από τον ίδιο τον ιστότοπο και όχι από τρίτους."),
            ("Φόρμα επικοινωνίας", "Η φόρμα στη σελίδα Επικοινωνίας δεν στέλνει τίποτα μέσω του ιστότοπου. Ετοιμάζει ένα email στη δική σας εφαρμογή email και τίποτα δεν αποστέλλεται μέχρι να πατήσετε αποστολή εκεί. Όταν μας γράφετε ή μας καλείτε, χρησιμοποιούμε τα στοιχεία σας μόνο για να απαντήσουμε στο αίτημά σας και να διαχειριστούμε την κράτησή σας."),
            ("Χάρτης", "Ο χάρτης παρέχεται από την Google και φορτώνει μόνο όταν το ζητήσετε. Από εκείνη τη στιγμή ισχύει η πολιτική απορρήτου της Google."),
            ("Κρατήσεις", "Όταν επιλέγετε «Κάντε κράτηση» μεταφέρεστε στο Booking.com, όπου ισχύουν οι δικοί του όροι και η δική του πολιτική απορρήτου."),
            ("Ερωτήσεις", "Για οτιδήποτε αφορά τα προσωπικά σας δεδομένα, γράψτε μας στο info@allofts.gr."),
        ],

        "nf_title": "Αυτή η σελίδα έκανε check-out.",
        "nf_p": "Η σελίδα που ψάχνετε δεν υπάρχει ή έχει μετακινηθεί.",
        "nf_home": "Επιστροφή στην αρχική",

        "moved": "Η σελίδα έχει μετακινηθεί.",

        "tags": {
            "living": "Καθιστικό", "bedroom": "Υπνοδωμάτιο", "kitchen": "Κουζίνα", "dining": "Τραπεζαρία",
            "bathroom": "Μπάνιο", "terrace": "Βεράντα", "balcony": "Μπαλκόνι", "garden": "Κήπος",
            "stairs": "Σκάλα", "detail": "Λεπτομέρεια", "net": "Δίχτυ χαλάρωσης", "view": "Άποψη του χώρου",
            "exterior": "Το κτίριο", "entrance": "Είσοδος", "lobby": "Κοινόχρηστοι χώροι", "roof": "Roof garden",
            "gym": "Γυμναστήριο", "aerial": "Αεροφωτογραφία",
        },
        "home_meta_title": "Allofts — Σύγχρονα lofts & σουίτες στην Καλαμάτα",
        "home_meta_desc": "Allofts: οκτώ lofts και σουίτες με ξεχωριστό χαρακτήρα στην Καλαμάτα, με roof garden και γυμναστήριο, κοντά στη θάλασσα. Ο χώρος σας, για να μείνετε, να ζήσετε, να εμπνευστείτε.",
    },
}

# ----------------------------------------------------------------------------
# Facilities (same wording as the original site)
# ----------------------------------------------------------------------------
FACILITIES = {
    "wifi":       {"en": "Wi-Fi",                      "el": "Wi-Fi"},
    "ac":         {"en": "Air conditioning",           "el": "Κλιματισμός"},
    "heating":    {"en": "Autonomous heating",         "el": "Αυτόνομη θέρμανση"},
    "kitchen":    {"en": "Kitchen",                    "el": "Κουζίνα"},
    "coffee":     {"en": "Coffee and tea facilities",  "el": "Παροχές καφέ & τσαγιού"},
    "minibar":    {"en": "Mini-bar",                   "el": "Mini-bar"},
    "tv":         {"en": "Flat-screen TV 40″",         "el": "Τηλεόραση επίπεδης οθόνης 40″"},
    "living":     {"en": "Living room",                "el": "Καθιστικό"},
    "furniture":  {"en": "Modern furniture",           "el": "Μοντέρνα επίπλωση"},
    "closet":     {"en": "Closet",                     "el": "Ντουλάπα"},
    "mirror":     {"en": "Full-length mirror",         "el": "Ολόσωμος καθρέφτης"},
    "shower":     {"en": "Shower",                     "el": "Μπάνιο με ντους"},
    "bath":       {"en": "Bathroom care products",     "el": "Προϊόντα περιποίησης μπάνιου"},
    "hairdryer":  {"en": "Hair dryer",                 "el": "Πιστολάκι μαλλιών"},
    "iron":       {"en": "Iron and ironing board",     "el": "Σίδερο και σιδερώστρα"},
    "soundproof": {"en": "Soundproof windows",         "el": "Παράθυρα με ηχομόνωση"},
    "locks":      {"en": "Electronic locks",           "el": "Ηλεκτρονικές κλειδαριές"},
    "cleaning":   {"en": "Room cleaning",              "el": "Καθαρισμός δωματίου"},
}
_BASE = ["wifi", "ac", "heating", "coffee", "minibar", "tv", "living", "furniture", "closet",
         "shower", "bath", "hairdryer", "soundproof", "locks", "cleaning"]
_ORDER = list(FACILITIES)
def _fac(*extra):
    keys = set(_BASE) | set(extra)
    return [k for k in _ORDER if k in keys]

# shown on the home page: what every single loft, suite and room has
COMMON_FACILITIES = ["wifi", "ac", "heating", "coffee", "minibar", "tv", "soundproof", "locks",
                     "bath", "hairdryer", "closet", "cleaning"]

# ----------------------------------------------------------------------------
# Lofts, suites and rooms.  Photos: (file inside ../photos/rooms/<slug>/, label)
# The first photo is the lead image.  Every photo listed for a room comes from
# that room's own page on the original site.
# ----------------------------------------------------------------------------
ROOMS = [
    {
        "slug": "executive-loft-i", "kind": "loft", "name": "Executive Loft I",
        "size": 55, "guests": 4, "sofa": 0, "extra": None,
        "facilities": _fac("kitchen", "iron", "mirror"),
        "tagline": {
            "en": "Double-height living, a floating staircase and a cocooning bedroom above.",
            "el": "Χώρος διπλού ύψους, μια αιωρούμενη σκάλα και ένα ζεστό υπνοδωμάτιο στο πατάρι.",
        },
        "desc": {
            "en": ["Welcome to our exquisite Executive Loft I, a spacious and luxurious retreat designed to accommodate up to four people. This exceptional 55 sq. m. loft offers an expansive living space and a fully equipped kitchen that seamlessly blends style, comfort and functionality, ensuring an unforgettable stay for you and your companions.",
                   "Our modern staircase leads you to a cocooning bedroom with an extra-comfortable queen-sized bed, ensuring a restful night’s sleep."],
            "el": ["Καλώς ήρθατε στο εξαίσιο Executive Loft I, ένα ευρύχωρο και πολυτελές διαμέρισμα σχεδιασμένο για να φιλοξενήσει έως και τέσσερα άτομα. Αυτό το εξαιρετικό loft 55 τ.μ. προσφέρει έναν άνετο χώρο καθιστικού και μια πλήρως εξοπλισμένη κουζίνα που συνδυάζει άψογα το στυλ, την άνεση και τη λειτουργικότητα, εξασφαλίζοντας μια αξέχαστη διαμονή για εσάς και την παρέα σας.",
                   "Η μοντέρνα σκάλα μας σάς οδηγεί σε μια κρεβατοκάμαρα με ένα εξαιρετικά άνετο κρεβάτι queen size, για έναν ξεκούραστο ύπνο. Ένα μεγάλο παράθυρο πλημμυρίζει τον χώρο με φυσικό φως και έχει θέα στον κήπο της βεράντας, δημιουργώντας μια φωτεινή και φιλόξενη ατμόσφαιρα."],
        },
        "photos": [
            ("20230810_211630.jpg", "living"),
            ("20230801_144634-scaled.jpg", "living"),
            ("20230801_143854-scaled.jpg", "bedroom"),
            ("received_825678172329299.jpeg", "view"),
            ("IMG_3612-1-scaled.jpg", "kitchen"),
            ("20230801_144103-scaled.jpg", "bedroom"),
            ("IMG_3654-scaled.jpg", "stairs"),
            ("IMG_3636-scaled.jpg", "living"),
            ("IMG_3627-scaled.jpg", "bathroom"),
            ("20230801_144027-scaled.jpg", "bedroom"),
            ("IMG_3631-scaled.jpg", "bathroom"),
            ("IMG_3664-scaled.jpg", "detail"),
        ],
    },
    {
        "slug": "executive-loft-ii", "kind": "loft", "name": "Executive Loft II",
        "size": 56, "guests": 4, "sofa": 0, "extra": None,
        "facilities": _fac("kitchen", "iron", "mirror"),
        "tagline": {
            "en": "Bright and calm, with a large window overlooking the terrace garden.",
            "el": "Φωτεινό και ήρεμο, με ένα μεγάλο παράθυρο που βλέπει στον κήπο της βεράντας.",
        },
        "desc": {
            "en": ["Welcome to our exquisite Executive Loft II, a spacious and luxurious retreat designed to accommodate up to four people. This exceptional 56 sq. m. loft offers an expansive living space and a fully equipped kitchen that seamlessly blends style, comfort and functionality, ensuring an unforgettable stay for you and your companions.",
                   "Our modern staircase leads you to a cocooning bedroom with an extra-comfortable queen-sized bed, ensuring a restful night’s sleep. A large window floods the space with natural light and overlooks the terrace garden, creating a bright and inviting ambiance."],
            "el": ["Καλώς ήρθατε στο εξαίσιο Executive Loft II, ένα ευρύχωρο και πολυτελές διαμέρισμα σχεδιασμένο για να φιλοξενήσει έως και τέσσερα άτομα. Αυτό το εξαιρετικό loft 56 τ.μ. προσφέρει έναν άνετο χώρο καθιστικού και μια πλήρως εξοπλισμένη κουζίνα που συνδυάζει άψογα το στυλ, την άνεση και τη λειτουργικότητα, εξασφαλίζοντας μια αξέχαστη διαμονή για εσάς και την παρέα σας.",
                   "Η μοντέρνα σκάλα μας σάς οδηγεί σε μια κρεβατοκάμαρα με ένα εξαιρετικά άνετο κρεβάτι queen size, για έναν ξεκούραστο ύπνο. Ένα μεγάλο παράθυρο πλημμυρίζει τον χώρο με φυσικό φως και έχει θέα στον κήπο της βεράντας, δημιουργώντας μια φωτεινή και φιλόξενη ατμόσφαιρα."],
        },
        "photos": [
            ("IMG_3613-1-1-scaled.jpg", "dining"),
            ("IMG_3616-1-scaled.jpg", "kitchen"),
            ("20230810_211104-scaled.jpg", "bedroom"),
            ("IMG_3674-scaled.jpg", "view"),
            ("IMG_3763-1-scaled.jpg", "bedroom"),
            ("IMG_3617-1-scaled.jpg", "dining"),
            ("IMG_3677-scaled.jpg", "bedroom"),
            ("IMG_3602-1-scaled.jpg", "dining"),
            ("1690218317607blob-1.png", "bedroom"),
            ("IMG_3626-1-scaled.jpg", "bathroom"),
            ("IMG_3877-scaled.jpg", "terrace"),
            ("IMG_3629-1-scaled.jpg", "bathroom"),
        ],
    },
    {
        "slug": "executive-loft-iii", "kind": "loft", "name": "Executive Loft III",
        "size": 49, "guests": 4, "sofa": 0, "extra": None,
        "facilities": _fac("kitchen", "iron", "mirror"),
        "tagline": {
            "en": "Black steel, marble and a crystal chandelier under a double-height ceiling.",
            "el": "Μαύρο μέταλλο, μάρμαρο και ένας κρυστάλλινος πολυέλαιος σε χώρο διπλού ύψους.",
        },
        "desc": {
            "en": ["Welcome to our exquisite Executive Loft III, a spacious and luxurious retreat designed to accommodate up to four people. This exceptional 49 sq. m. loft features a well-appointed living area, furnished with comfortable seating and modern amenities. A fully equipped kitchenette is conveniently integrated into the loft, allowing you to prepare and enjoy meals in the comfort of your own space.",
                   "Sink into the soft sofa and unwind after a day of exploring the city. The extra-large windows flood the space with natural light, creating a bright and inviting ambiance. The modern, floating metal staircase leads you to a luxurious master bedroom."],
            "el": ["Καλώς ήρθατε στο εξαίσιο Executive Loft III, ένα ευρύχωρο και πολυτελές διαμέρισμα 49 τ.μ., σχεδιασμένο για να φιλοξενήσει έως και τέσσερα άτομα. Το καθιστικό είναι άρτια εξοπλισμένο, με άνετα καθίσματα και σύγχρονες ανέσεις. Μια πλήρως εξοπλισμένη μικρή κουζίνα είναι βολικά ενσωματωμένη στο loft, ώστε να ετοιμάζετε και να απολαμβάνετε τα γεύματά σας στην άνεση του χώρου σας.",
                   "Βυθιστείτε στον αναπαυτικό καναπέ και χαλαρώστε μετά από μια μέρα εξερεύνησης της πόλης. Τα πολύ μεγάλα παράθυρα πλημμυρίζουν τον χώρο με φυσικό φως, δημιουργώντας μια φωτεινή και φιλόξενη ατμόσφαιρα. Η μοντέρνα, μεταλλική αιωρούμενη σκάλα σάς οδηγεί σε ένα πολυτελές κύριο υπνοδωμάτιο."],
        },
        "photos": [
            ("IMG_3526-scaled.jpg", "living"),
            ("IMG_3519-scaled.jpg", "living"),
            ("IMG_3552-scaled.jpg", "bedroom"),
            ("IMG_3548-scaled.jpg", "view"),
            ("IMG_3566-scaled.jpg", "kitchen"),
            ("IMG_3544-scaled.jpg", "living"),
            ("thumbnail-13.jpg", "bedroom"),
            ("IMG_3586-scaled.jpg", "living"),
            ("IMG_3573-scaled.jpg", "balcony"),
            ("IMG_3590-scaled.jpg", "stairs"),
            ("thumbnail-17.jpg", "bathroom"),
            ("IMG_3549-scaled.jpg", "view"),
        ],
    },
    {
        "slug": "executive-loft-iv", "kind": "loft", "name": "Executive Loft IV",
        "size": 49, "guests": 4, "sofa": 0, "extra": None,
        "facilities": _fac("kitchen", "iron", "mirror"),
        "tagline": {
            "en": "The artistic one: a suspended relaxation net and a bold black-and-white mural.",
            "el": "Το πιο καλλιτεχνικό: ένα αιωρούμενο δίχτυ χαλάρωσης και μια εντυπωσιακή ασπρόμαυρη τοιχογραφία.",
        },
        "desc": {
            "en": ["Welcome to our exquisite Executive Loft IV, a spacious and artistic retreat designed to accommodate up to four people. This exceptional 49 sq. m. loft features a well-appointed living area, furnished with comfortable seating and modern amenities. A fully equipped kitchenette is conveniently integrated into the loft, allowing you to prepare and enjoy meals in the comfort of your own space.",
                   "The centrepiece of the room is the relaxation net, thoughtfully suspended to create a unique and inviting feature. This hammock-like net is the perfect spot to unwind and let your worries drift away."],
            "el": ["Καλώς ήρθατε στο εξαίσιο Executive Loft IV, ένα ευρύχωρο και καλλιτεχνικό διαμέρισμα σχεδιασμένο για να φιλοξενήσει έως και τέσσερα άτομα. Αυτό το εξαιρετικό loft 49 τ.μ. διαθέτει όμορφα επιπλωμένο καθιστικό, με άνετα καθίσματα και σύγχρονες ανέσεις. Μια πλήρως εξοπλισμένη μικρή κουζίνα είναι ενσωματωμένη στο loft, ώστε να ετοιμάζετε και να απολαμβάνετε τα γεύματά σας στην άνεση του χώρου σας.",
                   "Το κεντρικό στοιχείο του χώρου είναι το δίχτυ χαλάρωσης, τοποθετημένο έτσι ώστε να δίνει έναν μοναδικό και φιλόξενο χαρακτήρα. Αυτό το κρεμαστό δίχτυ, που μοιάζει με αιώρα, είναι το τέλειο σημείο για να χαλαρώσετε και να αφήσετε πίσω ό,τι σας απασχολεί."],
        },
        "photos": [
            ("IMG_3821-scaled.jpg", "living"),
            ("IMG_3946-scaled.jpg", "net"),
            ("IMG_3832-scaled.jpg", "bedroom"),
            ("IMG_3816-scaled.jpg", "living"),
            ("IMG_3841-scaled.jpg", "bedroom"),
            ("IMG_3827-scaled.jpg", "living"),
            ("20230811_140813-scaled.jpg", "dining"),
            ("IMG_3725-scaled.jpg", "kitchen"),
            ("IMG_3740-scaled.jpg", "net"),
            ("IMG_3831-scaled.jpg", "detail"),
            ("20230814_141026-scaled.jpg", "bedroom"),
            ("thumbnail-29.jpg", "bathroom"),
        ],
    },
    {
        "slug": "eclectic-style-apartment", "kind": "apartment", "name": "Eclectic Style Apartment",
        "size": 45, "guests": 3, "sofa": 0, "extra": None,
        "facilities": _fac("kitchen", "iron"),
        "tagline": {
            "en": "A wallpapered feature wall, a mirrored door and a moody, modern kitchen.",
            "el": "Ένας εντυπωσιακός τοίχος με ταπετσαρία, μια πόρτα-καθρέφτης και μια μοντέρνα κουζίνα σε σκούρους τόνους.",
        },
        "desc": {
            "en": ["In this eclectic-style apartment, every detail reflects a curated blend of sophistication and creativity. As you step through the entrance, you’re immediately drawn into a space that exudes charm and character. The living area is a vibrant tapestry of colours and textures, featuring an eclectic mix of furnishings that seamlessly merge comfort with style. Sink into the plush sofa and take in the stunning feature wall, adorned with a mesmerising wallpaper that adds depth and character to the space.",
                   "The kitchen is a modern masterpiece, with sleek countertops and plenty of storage space.",
                   "As you make your way to the bedroom, you step through a modern mirror door. The bedroom itself is a sanctuary of comfort and style, with a luxurious queen-sized bed dressed in crisp linens and plush pillows. Large windows flood the room with natural light, creating a warm and inviting atmosphere.",
                   "With its eclectic charm and modern amenities, this apartment offers a stay of unparalleled elegance and sophistication. Welcome home to a world where every detail is a work of art."],
            "el": ["Σε αυτό το διαμέρισμα εκλεκτικού στυλ, κάθε λεπτομέρεια αντικατοπτρίζει έναν επιμελημένο συνδυασμό πολυτέλειας και δημιουργικότητας. Καθώς περνάτε την είσοδο, παρασύρεστε αμέσως σε έναν χώρο που αποπνέει γοητεία και χαρακτήρα. Το σαλόνι είναι ένα ζωντανό μωσαϊκό χρωμάτων και υφών, με έναν εκλεκτικό συνδυασμό επίπλων που ενώνουν άψογα την άνεση με το στυλ. Βυθιστείτε στον βελούδινο καναπέ και απολαύστε έναν εντυπωσιακό τοίχο διακοσμημένο με μια μαγευτική ταπετσαρία, που προσθέτει βάθος και χαρακτήρα στον χώρο.",
                   "Η μοντέρνα κουζίνα διαθέτει άνετους πάγκους και επαρκή αποθηκευτικό χώρο.",
                   "Καθώς κατευθύνεστε προς την κρεβατοκάμαρα, περνάτε μέσα από μια μοντέρνα πόρτα-καθρέφτη. Το ίδιο το υπνοδωμάτιο είναι ένα καταφύγιο άνεσης και στυλ, με ένα πολυτελές κρεβάτι queen size ντυμένο με πεντακάθαρα κλινοσκεπάσματα και βελούδινα μαξιλάρια. Τα μεγάλα ανοίγματα πλημμυρίζουν το δωμάτιο με φυσικό φως, δημιουργώντας μια ζεστή και φιλόξενη ατμόσφαιρα.",
                   "Με την εκλεκτική του γοητεία και τις σύγχρονες ανέσεις, αυτό το διαμέρισμα προσφέρει μια διαμονή απαράμιλλης κομψότητας και άνεσης."],
        },
        "photos": [
            ("IMG_1562-Copy-scaled.jpeg", "living"),
            ("IMG_1597-Copy-scaled.jpeg", "dining"),
            ("IMG_1362-Copy-scaled.jpeg", "bedroom"),
            ("IMG_1386-Copy-scaled.jpeg", "bathroom"),
            ("IMG_1390-Copy-scaled.jpeg", "living"),
            ("IMG_1621-Copy-scaled.jpeg", "bedroom"),
            ("IMG_1376-Copy-scaled.jpeg", "detail"),
            ("IMG_1379-Copy-scaled.jpeg", "dining"),
            ("IMG_1564-Copy-scaled.jpeg", "kitchen"),
            ("IMG_1371-Copy-scaled.jpeg", "bedroom"),
            ("IMG_1356-Copy-scaled.jpeg", "terrace"),
            ("IMG_4704-Copy.jpg", "bathroom"),
        ],
    },
    {
        "slug": "suite-room", "kind": "suite", "name": "Suite Room",
        "size": 40, "guests": 3, "sofa": 1, "extra": None,
        "facilities": _fac("kitchen", "iron"),
        "tagline": {
            "en": "Light-filled, with a steel-and-glass partition and a tall mustard headboard.",
            "el": "Γεμάτη φως, με διαχωριστικό από μέταλλο και γυαλί και ένα ψηλό κεφαλάρι στο χρώμα της μουστάρδας.",
        },
        "desc": {
            "en": ["The Suite Room offers a seamless fusion of style, comfort and functionality across 40 sq. m. of space. Sink into a queen-sized bed with a very comfortable mattress; the sofa bed can accommodate one extra guest.",
                   "Relax in the comfortable living area, prepare delicious meals in the fully equipped kitchen, and indulge in the privacy and comfort of your own stylishly furnished bedroom."],
            "el": ["Η σουίτα προσφέρει έναν μοναδικό συνδυασμό στυλ, άνεσης και λειτουργικότητας σε 40 τ.μ. Βυθιστείτε σε ένα κρεβάτι queen size με πολύ άνετο στρώμα· ο καναπές-κρεβάτι μπορεί να φιλοξενήσει 1 επιπλέον άτομο.",
                   "Χαλαρώστε στον άνετο χώρο του καθιστικού, ετοιμάστε νόστιμα γεύματα στην πλήρως εξοπλισμένη κουζίνα και απολαύστε την ιδιωτικότητα και την άνεση του δικού σας κομψά επιπλωμένου υπνοδωματίου."],
        },
        "photos": [
            ("20230830_132247-scaled.jpg", "living"),
            ("20230830_131951-scaled.jpg", "living"),
            ("foto-alloft4.jpg", "bedroom"),
            ("20230830_132044-scaled.jpg", "living"),
            ("20230830_132356-scaled.jpg", "view"),
            ("fot-oalloft6.jpg", "bedroom"),
            ("20230830_132107-scaled.jpg", "living"),
            ("foto-alloft1.jpg", "balcony"),
            ("foto-alloft7.jpg", "bedroom"),
            ("287246857_711704339883300_2235717751201319659_n.jpg", "bathroom"),
        ],
    },
    {
        "slug": "suite-room-with-garden", "kind": "suite", "name": "Suite Room with Garden",
        "size": 40, "guests": 4, "sofa": 2, "extra": "garden",
        "facilities": _fac("kitchen", "iron", "mirror"),
        "tagline": {
            "en": "A calm suite that opens onto a small garden of its own.",
            "el": "Μια ήρεμη σουίτα που ανοίγει στον δικό της μικρό κήπο.",
        },
        "desc": {
            "en": ["Welcome to our spacious and inviting suite with a delightful small garden, a tranquil oasis for your stay. With a generous 40 sq. m. of well-designed space and a fully equipped kitchen, it is perfect for couples seeking comfort and relaxation.",
                   "Sink into a queen-sized bed with a very comfortable mattress; the sofa bed can accommodate two extra guests."],
            "el": ["Καλώς ήρθατε στην ευρύχωρη και φιλόξενη σουίτα μας με έναν υπέροχο μικρό κήπο, μια ήρεμη όαση για τη διαμονή σας. Με 40 τ.μ. καλοσχεδιασμένου χώρου και πλήρως εξοπλισμένη κουζίνα, είναι ιδανική για ζευγάρια που αναζητούν άνεση και χαλάρωση.",
                   "Βυθιστείτε σε ένα κρεβάτι queen size με πολύ άνετο στρώμα· ο καναπές-κρεβάτι μπορεί να φιλοξενήσει 2 επιπλέον άτομα."],
        },
        "photos": [
            ("287384203_1147669749347267_5827634354737777001_n.jpg", "living"),
            ("287184525_3209815819261138_4925834004959902072_n.jpg", "garden"),
            ("286892074_2823767291250576_8377246396252274814_n.jpg", "bedroom"),
            ("287182767_562307088900157_7802073621030174674_n.jpg", "living"),
            ("286987796_573579407455750_3139884854347023184_n.jpg", "garden"),
            ("286832406_414909437177154_2001475721643866833_n.jpg", "bedroom"),
            ("287089766_598233668105007_2490052471412117848_n.jpg", "detail"),
            ("287361153_531950921963378_1644041045998892563_n.jpg", "bathroom"),
        ],
    },
    {
        "slug": "separated-premium-room", "kind": "room", "name": "Separated Premium Room",
        "size": 28, "guests": 2, "sofa": 0, "extra": "terrace",
        "facilities": _fac(),
        "tagline": {
            "en": "Olive green, warm orange and a floral headboard, with a planted terrace of its own.",
            "el": "Πράσινο της ελιάς, ζεστό πορτοκαλί και ένα λουλουδάτο κεφαλάρι, με τη δική του βεράντα με φυτά.",
        },
        "desc": {
            "en": ["Step into a room that radiates joy and vitality. The walls are painted in cheerful shades of olive green and orange.",
                   "The centrepiece of the room is undoubtedly the bed, with its headboard transformed into a breathtaking floral tapestry — a work of art, like a garden in bloom above the bed.",
                   "You can also enjoy your coffee on the beautiful terrace decorated with plants. This separated room offers the perfect balance of comfort, style and privacy, providing a tranquil retreat. Whether you’re travelling for business or pleasure, it’s a space where you can truly relax and escape the monotony of everyday life."],
            "el": ["Το δωμάτιο εκπέμπει χαρά και ζωντάνια. Οι τοίχοι είναι βαμμένοι σε χαρούμενες αποχρώσεις του πράσινου της ελιάς και του πορτοκαλί.",
                   "Το κεντρικό στοιχείο του δωματίου είναι αναμφίβολα το κρεβάτι, με το κεφαλάρι του να έχει μεταμορφωθεί σε μια συναρπαστική λουλουδάτη ταπισερί.",
                   "Μπορείτε επίσης να απολαύσετε τον καφέ σας στην όμορφη βεράντα, που είναι διακοσμημένη με φυτά. Αυτό το ξεχωριστό δωμάτιο προσφέρει την τέλεια ισορροπία άνεσης, στυλ και ιδιωτικότητας, ένα ήρεμο καταφύγιο. Είτε ταξιδεύετε για επαγγελματικούς λόγους είτε για αναψυχή, είναι ένας χώρος όπου μπορείτε πραγματικά να χαλαρώσετε και να ξεφύγετε από τη μονοτονία της καθημερινότητας."],
        },
        "photos": [
            ("IMG_1510-Copy-scaled.jpeg", "bedroom"),
            ("IMG_1454-Copy-scaled.jpeg", "bedroom"),
            ("IMG_1547-Copy-scaled.jpeg", "terrace"),
            ("IMG_1453-Copy-scaled.jpeg", "bedroom"),
            ("IMG_1480-Copy-scaled.jpeg", "bedroom"),
            ("IMG_1555-Copy-scaled.jpeg", "living"),
            ("IMG_1542-Copy-scaled.jpeg", "terrace"),
            ("IMG_1503-Copy-scaled.jpeg", "detail"),
            ("IMG_1532-Copy-scaled.jpeg", "terrace"),
            ("IMG_1477-Copy-scaled.jpeg", "bathroom"),
        ],
    },
]

EXTRA = {
    "garden":  {"en": "Small garden", "el": "Μικρός κήπος"},
    "terrace": {"en": "Terrace",      "el": "Βεράντα"},
}

# ----------------------------------------------------------------------------
# Photos of the house itself: id -> (file inside ../photos, label)
# ----------------------------------------------------------------------------
HOUSE = {
    "ext-day":      ("gallery/IMG_3779-scaled.jpg", "exterior"),
    "ext-entrance": ("gallery/IMG_3780-scaled.jpg", "entrance"),
    "ext-dusk":     ("home/ALLOFTS-OUY.png", "exterior"),
    "ext-night":    ("gallery/received_600867608631477.jpeg", "exterior"),
    "ext-sign":     ("gallery/received_309353661500210-1.jpeg", "entrance"),
    "ext-tree":     ("gallery/received_542151648037511-1.jpeg", "exterior"),
    "ext-garden":   ("gallery/IMG_1336-Copy-scaled.jpeg", "exterior"),
    "ext-detail":   ("gallery/IMG_1344-Copy-scaled.jpeg", "exterior"),
    "ext-angle":    ("rooms/separated-premium-room/IMG_1526-Copy-scaled.jpeg", "exterior"),
    "in-corridor":  ("gallery/received_1695527150947802.jpeg", "entrance"),
    "in-door":      ("gallery/received_824723919300521.jpeg", "entrance"),
    "in-lobby":     ("gallery/received_625317939415759.jpeg", "lobby"),
    "in-stairs-1":  ("gallery/received_867154344244095.jpeg", "lobby"),
    "in-stairs-2":  ("gallery/received_6547045752078146.jpeg", "lobby"),
    "roof-deck":    ("gallery/thumbnail-13.jpg", "roof"),
    "roof-lounge":  ("gallery/thumbnail-10.jpg", "roof"),
    "roof-table":   ("gallery/thumbnail-17.jpg", "roof"),
    "roof-bar":     ("gallery/thumbnail-18.jpg", "roof"),
    "roof-view":    ("gallery/thumbnail-19.jpg", "roof"),
    "roof-wide":    ("gallery/thumbnail-20.jpg", "roof"),
    "roof-sunset":  ("gallery/thumbnail-21.jpg", "roof"),
    "roof-moon":    ("gallery/thumbnail-9.jpg", "roof"),
    "roof-drone":   ("gallery/DRONE-ΜΕΤΑΤΡΟΠΗ.jpg", "aerial"),
    "gym-room":     ("gallery/thumbnail-24.jpg", "gym"),
    "gym-bikes":    ("gallery/359521673_655780163102114_7216424031261829507_n.jpg", "gym"),
    "aerial":       ("home/DJI_0060-1.jpg", "aerial"),
    "loft-chandelier": ("gallery/20230811_141007-scaled.jpg", "view"),
    "loft-stairs":  ("gallery/received_617953820192138.jpeg", "view"),
    "loft-kitchen": ("gallery/received_270585549087279.jpeg", "view"),
    "loft-mezz":    ("gallery/received_1334491670485798.jpeg", "bedroom"),
    "suite-glass":  ("gallery/286876412_348656727409508_2591854622576086649_n.jpg", "view"),
    "breakfast":    ("gallery/IMG_3656-scaled.jpg", "detail"),
}

# Home page opening slides: (room slug, photo number in that room's list starting at 1,
#   focus on wide screens (x, y from 0 to 1), focus on phones (x, y))
HERO = [
    ("executive-loft-iii", 1, (0.50, 0.62), (0.30, 0.50)),
    ("executive-loft-iv", 1, (0.50, 0.55), (0.60, 0.50)),
    ("executive-loft-i", 1, (0.50, 0.60), (0.45, 0.50)),
    ("separated-premium-room", 1, (0.50, 0.65), (0.55, 0.50)),
    ("eclectic-style-apartment", 1, (0.50, 0.60), (0.60, 0.50)),
]

# Gallery page.  Room photos are given as (room slug, photo number); house photos by id.
GALLERY = [
    ("lofts", ("executive-loft-iii", 1)), ("roof", "roof-deck"), ("lofts", ("executive-loft-iv", 2)),
    ("house", "ext-day"), ("lofts", ("eclectic-style-apartment", 1)), ("lofts", ("executive-loft-i", 1)),
    ("lofts", ("separated-premium-room", 1)), ("roof", "roof-view"), ("lofts", ("suite-room", 1)),
    ("lofts", "loft-chandelier"), ("house", "ext-night"), ("lofts", ("executive-loft-ii", 1)),
    ("lofts", ("executive-loft-iv", 1)), ("lofts", ("suite-room-with-garden", 2)), ("roof", "roof-lounge"),
    ("lofts", ("executive-loft-iii", 4)), ("house", "ext-entrance"), ("lofts", ("eclectic-style-apartment", 4)),
    ("lofts", ("executive-loft-i", 3)), ("lofts", ("separated-premium-room", 2)), ("roof", "roof-table"),
    ("lofts", ("suite-room", 3)), ("house", "in-corridor"), ("lofts", ("executive-loft-ii", 3)),
    ("lofts", ("executive-loft-iv", 3)), ("lofts", "loft-stairs"), ("roof", "roof-sunset"),
    ("lofts", ("eclectic-style-apartment", 2)), ("house", "ext-dusk"), ("lofts", ("executive-loft-iii", 3)),
    ("lofts", ("suite-room-with-garden", 1)), ("lofts", ("separated-premium-room", 3)), ("roof", "roof-bar"),
    ("lofts", ("executive-loft-i", 2)), ("house", "in-stairs-1"), ("lofts", ("executive-loft-iv", 9)),
    ("lofts", ("executive-loft-ii", 2)), ("lofts", "suite-glass"), ("roof", "roof-drone"),
    ("lofts", ("eclectic-style-apartment", 3)), ("house", "in-lobby"), ("lofts", ("executive-loft-iii", 5)),
    ("lofts", ("suite-room", 2)), ("roof", "gym-room"), ("lofts", "loft-kitchen"),
    ("house", "ext-sign"), ("lofts", ("suite-room-with-garden", 3)), ("roof", "roof-wide"),
    ("lofts", ("executive-loft-i", 7)), ("house", "ext-garden"), ("lofts", "breakfast"),
    ("house", "in-stairs-2"), ("roof", "roof-moon"), ("lofts", "loft-mezz"),
    ("house", "ext-angle"), ("roof", "gym-bikes"), ("house", "ext-tree"),
]

# Guest reviews, as published on the original site
REVIEWS = [
    {"name": "Razvan", "from": {"en": "Romania", "el": "Ρουμανία"}, "lang": "en",
     "text": "The room was spotless, with a very cozy and warm atmosphere. It was very kindly decorated, making you feel very comfortable and just like home. Lots of spaces to deposit clothes, making the stay even more enjoyable."},
    {"name": "Gabriel", "from": {"en": "United Kingdom", "el": "Ηνωμένο Βασίλειο"}, "lang": "en",
     "text": "The property looks amazing and it has a modern design, loved the little terrace/patio area, the staff are professional, helpful and very lovely."},
    {"name": "Άννα", "name_en": "Anna", "from": {"en": "Greece", "el": "Ελλάδα"}, "lang": "el",
     "text": "Το διαμέρισμα ήταν πολύ καθαρό, άνετο, άψογα διακοσμημένο και εξοπλισμένο. Πολύ ξεχωριστό και το μπαλκόνι του! Πολύ κοντά στην παραλία. Ευγενέστατοι οι οικοδεσπότες. Θα το επιλέγαμε σίγουρα ξανά!",
     "text_en": "The apartment was very clean, comfortable, impeccably decorated and equipped. Its balcony is something special too! Very close to the beach. The hosts were extremely kind. We would definitely choose it again!"},
]
