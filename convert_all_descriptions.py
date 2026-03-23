#!/usr/bin/env python3
import json

# Load the Hindi JSON
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi_data = json.load(f)

print("=" * 70)
print("COMPREHENSIVE HINDI DESCRIPTION CONVERSION")
print("=" * 70)

# Manual translations for English descriptions that need to be converted to Hindi
english_to_hindi_descriptions = {
    "With senses, mind & intellect under control, liberated soul is free from desire, fear, anger": "इंद्रियों, मन और बुद्धि पर नियंत्रण से मुक्त आत्मा इच्छा, भय और क्रोध से मुक्त है",
    "Krishn is the enjoyer of all sacrifices & austerities, also the selfless friend of all beings": "कृष्ण सभी यज्ञों और तपस्याओं के भोक्ता हैं, साथ ही सभी प्राणियों के निःस्वार्थ मित्र हैं",
    "Doing duty without expecting Fruits, not just giving up fire or action, is a Yogi or Sanyasi": "फल की अपेक्षा किए बिना कर्तव्य करना, केवल अग्नि या कर्म का त्याग नहीं, एक योगी या संन्यासी है",
    "Sanyasi is a Yogi who has given up thoughts of worldly desires": "संन्यासी एक योगी है जिसने सांसारिक इच्छाओं के विचार त्याग दिए हैं",
    "Without KarmYog, SankhyYog is difficult to get and KarmYogi reaches Brahm soon": "कर्म योग के बिना, साँख्य योग प्राप्त करना कठिन है और कर्म योगी जल्द ब्रह्म तक पहुँचता है",
    "With mind & intellect merged in Him, sins get wiped out and reach the state of no return": "मन और बुद्धि उसमें विलीन होकर पाप मिट जाते हैं और कोई वापसी नहीं है",
    "With mind disciplined, constantly engaged in God, attains the supreme efflugent; divine Purush": "मन को अनुशासित करके, निरंतर ईश्वर में लगा हुआ, परम तेजस्वी दिव्य पुरुष को प्राप्त करता है",
    "With your mind established in Yog, you will attain Krishn": "योग में आपके मन की स्थिति से आप कृष्ण को प्राप्त करेंगे",
    "With insatiable desires and ignorance, demonic people with impure conduct are full of hypocrisy, pride and ignorance": "अतृप्त इच्छाओं और अज्ञान से, दुष्ट प्रकृति के लोग अपवित्र आचरण, पाखंड, गर्व और अज्ञान से भरे हुए हैं",
    "With unending cares for life, they remain devoted to sensuous pleasures, believing those to be the limit of joy": "जीवन की अंतहीन चिंताओं के साथ, वे सुख-भोगों के प्रति समर्पित रहते हैं, उन्हें आनंद की सीमा मानते हुए",
    "With many ties of expectations, lust and anger, they strive to amass wealth and objects of sensuous pleasures by unfair means": "आशाओं, काम और क्रोध के कई बंधनों से, वे अनुचित तरीकों से धन और इंद्रिय भोगों को जमा करने का प्रयास करते हैं",
    "Krishn reciprocates the way and form of worship one adopts": "कृष्ण जिस तरीके और रूप में पूजा की जाती है, वैसे ही प्रतिफल देते हैं",
    "Men seeking fruits, worship Gods for quick success of their actions": "फल चाहने वाले मनुष्य अपने कार्यों की जल्दी सफलता के लिए देवताओं की पूजा करते हैं",
    "Four orders of the society were created basis Gunas predominant and thus duties": "समाज के चार वर्ण प्रधान गुणों के आधार पर बनाए गए थे और इसलिए कर्तव्य भी",
    "Krishn is not tainted by actions and one who knows him is not bound by actions": "कृष्ण कर्मों से प्रभावित नहीं हैं और जो उन्हें जानता है वह भी कर्मों से बंधा नहीं है",
    "Action was performed even by the ancient seekers of liberation": "मुक्ति के प्राचीन साधकों द्वारा भी कर्म किए जाते थे",
    "Knowing the difference between action and inaction, get free from the evil effects": "कर्म और अकर्म के बीच का अंतर जानकर, बुरे प्रभावों से मुक्त हो जाएं",
    "Know the mysterious ways of action, inaction and prohibited actions": "कर्म, अकर्म और निषिद्ध कर्मों के रहस्यमय तरीकों को जानें",
    "Yogi sees action in inaction and vice versa, such wise perform all actions": "योगी क्रियाहीनता में क्रिया देखता है और विपरीत रूप में भी, ऐसे ज्ञानी सभी कर्म करते हैं",
    "Undertakings free from desire and worldly thoughts, with actions burnt up by wisdom": "इच्छा और सांसारिक विचारों से मुक्त उद्योग, ज्ञान द्वारा जले हुए कर्मों के साथ",
    "No attachment to actions or fruits, no dependence, ever content, yet fully engaged": "कर्मों या फलों से कोई लगाव नहीं, कोई निर्भरता नहीं, हमेशा संतुष्ट, फिर भी पूरी तरह लगा हुआ",
    "No sin in bodily actions with subdued mind & body, free from craving and enjoyments": "अपने आप को नियंत्रित करने वाले मन और शरीर के साथ शारीरिक कर्मों में कोई पाप नहीं, तृष्णा और भोग से मुक्त",
    "Content, free from jealousy, joy & sorrow, equipoised in success & failure, not bound": "संतुष्ट, ईर्ष्या से मुक्त, आनंद और दुख से समान, सफलता और विफलता में समभाव, बंधा नहीं",
    "Actions melt away, free from attachment, beyond body, mind in self, works for sacrifice": "कर्म पिघल जाते हैं, लगाव से मुक्त, शरीर से परे, मन आत्मा में, यज्ञ के लिए काम करता है",
    "Brahm is the ladle, oblation, fire, sacrificer and the goal of the one absorbed in Brahm": "ब्रह्म ही घी, अन्न, आग, यजमान और ब्रह्म में लीन होने वाले का लक्ष्य है",
    "Yogis offer worship as sacrifice, others offer self in the fire of Brahm": "योगी पूजा को यज्ञ के रूप में चढ़ाते हैं, अन्य आत्मा को ब्रह्म की आग में चढ़ाते हैं",
    "Few Yogis offer senses in the fire of discipline, others offer objects into fire of senses": "कुछ योगी इंद्रियों को अनुशासन की आग में चढ़ाते हैं, अन्य वस्तुओं को इंद्रियों की आग में",
    "KarmYogi with conquered mind & senses, pure heart, identifying self, stays untainted": "विजित मन और इंद्रियों वाला कर्म योगी, शुद्ध हृदय, आत्म-पहचान के साथ, निर्लिप्त रहता है",
    "SankhyYogi knows the reality and must believe that he does nothing in any action": "साँख्य योगी वास्तविकता को जानता है और विश्वास करता है कि किसी भी कर्म में वह कुछ नहीं करता",
    "It is the senses alone that are moving among their objects": "केवल इंद्रियाँ ही अपनी वस्तुओं के बीच चलती हैं",
    "Offering all actions to the Almighty and having no attachment, untouched by sin": "सभी कर्मों को सर्वशक्तिमान को समर्पित करना और कोई लगाव न होना, पाप से अछूता",
    "KarmYogi performs actions without sense of mine, only for self-purification": "कर्म योगी 'मेरा' की भावना के बिना कर्म करता है, केवल आत्म-शुद्धि के लिए",
    "Offering the fruits of action to the Supreme, KarmYogi attains everlasting peace": "कर्मों के फल को परम को समर्पित करके, कर्म योगी शाश्वत शांति पाता है",
    "Self controlled SankhyYogi rests happily doing nothing, mentally relegating all actions": "आत्म-नियंत्रित साँख्य योगी कुछ न करते हुए खुशी से विश्राम करता है, मानसिक रूप से सभी कर्मों को त्याग देता है",
    "Nature alone determines the doership, contact of actions and fruits; not the Supreme": "प्रकृति ही कर्ता, कर्मों का संपर्क और फल निर्धारित करती है, परम नहीं",
    "The Supreme doesn't receive virtue or sin of anyone and ignorance covers knowledge": "परम किसी का पुण्य या पाप प्राप्त नहीं करता और अज्ञान ज्ञान को ढक देता है",
    "Wisdom shining like the sun reveals the Supreme and destroys ignorance": "ज्ञान सूर्य की तरह चमकता हुआ परम को प्रकट करता है और अज्ञान को नष्ट करता है",
    "The wise look equanimity on all, including Brahmin, Cow, Elephant, Dog or a pariah": "ज्ञानी सभी को समान दृष्टि से देखते हैं, ब्राह्मण, गाय, हाथी, कुत्ता या चांडाल सभी को",
    "Mind with equanimity conquers the mortal plane and is established in the Brahm": "समभाव वाला मन नश्वर लोक को जीत लेता है और ब्रह्म में स्थापित हो जाता है",
    "One with reasoning and no doubt, neither rejoices nor gets purturbed, lives eternally": "तर्क और कोई संदेह न रखने वाला न तो आनंदित होता है न विचलित, शाश्वत जीता है",
    "Not attached to sense-objects, derives Sattvik joy, that Yogi enjoys eternal bliss": "इंद्रिय-वस्तुओं से लगाव न रखते हुए, सात्विक आनंद प्राप्त करता है, ऐसा योगी शाश्वत आनंद भोगता है",
    "Pleasures out of sense-contacts bring suffering, hence wise men don't indulge in": "इंद्रिय-संपर्क से मिलने वाले सुख दुख लाते हैं, इसलिए ज्ञानी उनमें लिप्त नहीं होते",
    "One who can withstand the urge of lust and anger, is a Yogi and a happy man": "जो काम और क्रोध की वृत्ति को सहन कर सकता है, वह योगी है और सुखी मनुष्य है",
    "A Yogi is happy, enjoying, delighted and illumined with self; thus attains Brahm & peace": "एक योगी आनंदी है, भोगी है, प्रसन्न है और आत्मा से प्रकाशित है, इस तरह ब्रह्म और शांति को प्राप्त करता है",
    "Seers with sins and doubts destroyed, mind disciplined, actively engage in service": "पाप और संदेह नष्ट होने वाले दर्शी, मन अनुशासित, सक्रिय रूप से सेवा में लगे हुए",
    "Wise men free of lust and anger, subdue mind and attain Supreme the eternal peace": "काम और क्रोध से मुक्त ज्ञानी, मन को वश करके, परम को प्राप्त करते हैं - शाश्वत शांति",
    "Shutting thoughts of enjoyment, gaze fixed in the middle and regulated breaths": "भोग के विचारों को बंद करके, निगाह बीच में रखते हुए और सांस को नियंत्रित करते हुए",
    "Practicing Yog with mind attached & absolute dependence on Krishn, you'll know him in the entirety": "मन को कृष्ण से लगाकर और पूर्ण निर्भरता के साथ योग का अभ्यास करते हुए, आप उन्हें पूरी तरह जान जाएंगे",
    "God shall unfold the entirety of wisdom with the knowledge of qualified aspect of god": "ईश्वर की योग्य पहलू के ज्ञान से ईश्वर सभी ज्ञान को उजागर करेंगे",
    "What is sprituality?": "आध्यात्मिकता क्या है?",
    "Who is Adhiyagna, and how does one with a steadfast mind realise God at death?": "अधियज्ञ कौन है, और दृढ़ मन वाला कैसे मृत्यु समय ईश्वर को प्राप्त करता है?",
    "The supreme indestruvtible is Brahm": "परम अविनाशी ब्रह्म है",
    "Krishn himself, dwelling as the inner witness, is Adhiyagna. Perishables are Adhibhut; Shining Purush is Adhidaiv": "कृष्ण स्वयं, आंतरिक साक्षी के रूप में निवास करते हुए, अधियज्ञ हैं। नाशवान वस्तुएं अधिभूत हैं; प्रकाशमान पुरुष अधिदैव है",
    "He who thinks of Krishn even at the time of death, attains Krishn's state": "जो मृत्यु के समय भी कृष्ण का ध्यान करता है, वह कृष्ण की अवस्था को प्राप्त करता है",
    "Attains what at the time of death, absorbs in its thought": "मृत्यु के समय जिस बात में मन लीन हो, उसी को प्राप्त करता है",
}

converted = 0
for shlok in hindi_data:
    if "__8" in shlok:
        current_desc = shlok["__8"].strip()
        if current_desc in english_to_hindi_descriptions:
            shlok["__8"] = english_to_hindi_descriptions[current_desc]
            converted += 1

print(f"\n✓ Converted {converted} English descriptions to Hindi!")

# Save the updated file
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi_data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 70)
print("✓ SUCCESS! Hindi JSON file now has Hindi descriptions!")
print("=" * 70)
print("\nNext: flutter clean && flutter run -d ZD22267824")
