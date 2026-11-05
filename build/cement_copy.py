# -*- coding: utf-8 -*-
"""Cement microsite copy, English and Arabic.

Voice is taken from the CEO's website master copy: context, workflow, inputs,
coordinate, configure, enterprise. No em dashes. Canadian spelling.
Both language dicts carry identical keys; cement.py asserts that.

The Arabic is stored as literal UTF-8 so a native speaker can read and edit it
here directly. It has had one adversarial review pass; it still wants a human
native-speaker read before any campaign points at it.
"""

EN = {
 'lang': 'en',
 'dir': 'ltr',
 'other': 'ar',
 'other_label': 'العربية',
 'self_label': 'EN',
 'nav': [
          ('About', 'index.html#about'),
          ('Cement Context', 'index.html#context'),
          ('Platform', 'platform.html'),
          ('Events', 'events.html'),
        ],
 'nav_cta': 'Discuss Your Needs',
 'skip': 'Skip to content',
 'by': 'TwoSuns by AEPG',
 'foot_links': [
                 ('About', 'index.html#about'),
                 ('Cement Context', 'index.html#context'),
                 ('Platform', 'platform.html'),
                 ('Events', 'events.html'),
                 ('Discuss Your Needs', 'https://twosuns.ai/discuss.html'),
               ],
 'foot_email': 'info@twosuns.ai',
 'foot_wa': 'WhatsApp +1 250 859 6563',
 'foot_rights': '© 2026 TwoSuns by AEPG. All rights reserved.',
 'foot_privacy': 'Privacy',
 'foot_terms': 'Terms',
 'main_site': 'twosuns.ai',
 'home_title': 'TwoSuns for Cement | Shared enterprise context from quarry to cash',
 'home_desc': "An adaptive enterprise platform configured around cement. TwoSuns coordinates "
               "quarry, kiln, mill, dispatch and sales through shared enterprise context.",
 'home_eyebrow': 'Adaptive enterprise capability for cement producers',
 'home_h1': "Grow, operate and coordinate complex work through shared enterprise context.",
 'home_sub': "TwoSuns is an adaptive enterprise platform for the built industry, configured "
              "here around cement. It combines the inputs a plant already records, "
              "context-aware intelligence, agentic support and configurable workflows, so "
              "process, quality, commercial and finance teams coordinate from the same "
              "context.",
 'home_cta1': 'Discuss Your Needs',
 'home_cta2': 'Explore the Platform',
 'about_tag': 'About TwoSuns',
 'about_h': 'Enterprise experience applied to the work of a cement producer',
 'about_p1': "TwoSuns brings together enterprise strategy, product leadership, industry "
              "knowledge, growth expertise, analytics, software engineering, artificial "
              "intelligence, data engineering and implementation capability. The platform is "
              "developed by AEPG in Canada and configured with the producer's own process, "
              "quality and commercial leads.",
 'about_p2': "We build practical enterprise capability out of connected context, intelligence "
              "and configurable workflows. In cement that capability runs from the quarry face "
              "to cash collected, and the work is carried out by functions that each hold their "
              "own authority.",
 'about_fam_h': 'One platform across the plant and the market',
 'fams': [
           (
             'Core',
             'The shared enterprise context, configuration and continuity layer.',
             'Plant basis, operating limits, roles, approval chains and decision history.',
           ),
           (
             'Ray',
             'Context-aware assistance available throughout the platform.',
             "Explanation, synthesis and workflow support, within each user's permissions.",
           ),
           (
             'Horizon',
             'Market, growth, relationship and commercial capabilities.',
             "Strategy and product market fit, signals, plays, contracts and offers, orders "
              "and invoicing, finance.",
           ),
           (
             'Pulse',
             'Product, project, operational and asset capabilities.',
             "Quarry, materials and supply, raw mix, pyro process, grinding, packing and "
              "dispatch, sustainability.",
           ),
         ],
 # the platform architecture figure on the home page, drawn by arch.py
 'arx_tag': 'Architecture',
 'arx_h': 'Enterprise context becomes coordinated action',
 'arx_p': 'Commercial intelligence and operational execution, connected through one governed enterprise context.',
 'arx_foot': 'One governed context. Two operating domains. Continuous enterprise awareness.',
 'arx_cta': 'Explore the Platform',
 'arx_labels': {
                 'core_1': 'Governance and permissions',
                 'core_2': 'Organizational memory and logs',
                 'core_3': 'Decision continuity',
                 'core_k': 'Governed context',
                 'flow_in': 'Context in',
                 'flow_out': 'Coordinated action out',
                 'hz_1': 'Market and account intelligence',
                 'hz_2': 'Revenue coordination',
                 'hz_3': 'GTM execution',
                 'hz_k': 'Commercial intelligence',
                 'orb_customers': 'Customers',
                 'orb_markets': 'Markets',
                 'orb_operations': 'Operations',
                 'orb_people': 'People and systems',
                 'pl_1': 'Operational workflows',
                 'pl_2': 'Supply and resource coordination',
                 'pl_3': 'Performance management',
                 'pl_k': 'Operational execution',
                 'ray_1': 'Contextual continuity',
                 'ray_2': 'Enterprise awareness',
                 'ray_3': 'Coordinated action',
                 'ray_sub': 'Persistent enterprise companion',
                 'svg_aria': 'Horizon and Pulse as two operating domains, Core as the governed context between them, Ray spanning beneath.',
               },
 'ctx_tag': 'Cement Context',
 'ctx_h': 'Cost per tonne is set by decisions taken in separate functions',
 'ctx_p1': "A cement plant takes many decisions each day that move cost per tonne: which "
            "faces feed the crusher, how the raw mix is corrected, which fuels are fired, "
            "which silos are released, and which tonnes and prices sales commits. Each one "
            "sits with a different function and a different system.",
 'ctx_p2': "TwoSuns brings those decisions into one enterprise environment alongside the "
            "systems already in place. Each function keeps its authority and sees what its "
            "decision does to cost, capacity, stock and quality elsewhere in the business.",
 'ctx_cond_h': 'Conditions shared across cement operations',
 'ctx_cond': [
               'Long quarry, kiln and asset lifecycles',
               'Many functions contributing to one tonne',
               'Regional requirements, permits and operating practices',
               'Complex commercial, technical and regulatory relationships',
               'Physical, financial, market and operational inputs',
               'Frequent handoffs across functional boundaries',
               'Continuing value long after the tonne is produced',
             ],
 'ctx_flow_h': 'Follow the workflow across the plant',
 'ctx_flow_p': "A change at the quarry face moves raw mix correction, kiln heat, clinker "
                "quality, cement strength, the tonnes dispatch can release and the prices "
                "sales can commit. An export order accepted on Monday sets grinding, packing "
                "and stock decisions for the rest of the week. A cement business is connected "
                "through these continuing workflows, and the platform is configured around "
                "them.",
 'cfg_tag': 'Configuration',
 'cfg_h': 'Configure TwoSuns around your plant',
 'cfg_p': "Plants with similar kilns can need different decisions on the same day. Each "
           "deployment is shaped around the plant's own basis, its operating environment, "
           "users, regions, inputs, integrations and expected value, and is configured with "
           "the process, quality and commercial leads before the platform produces a "
           "recommendation.",
 'cfg_rows': [
               (
                 'Plant and lines',
                 'Kiln lines, mills, packers and silos, with their operating limits',
               ),
               (
                 'Raw materials and fuels',
                 "Quarry and corrective chemistry, and fuels with their calorific value, "
                  "sulphur, chlorine and ash",
               ),
               (
                 'Standards and permits',
                 "Cement classes produced, stack permits, fuel licences, export and carbon "
                  "reporting",
               ),
               (
                 'Organization and approvals',
                 'Roles, reporting lines, approval chains and authority levels',
               ),
               ('Markets', 'Regions, channels, customers and export destinations'),
               (
                 'Inputs',
                 "Historian, laboratory, ERP, weighbridge and surveys, and how often each "
                  "arrives",
               ),
             ],
 'home_close_h': 'Begin with the decision that matters now',
 'home_close_p': "TwoSuns is developed in Canada. The team is in Cairo from 10 to 26 November "
                  "and can meet at your plant or office to review one decision against your "
                  "own reports, under a mutual NDA.",
 'home_close_cta1': 'Request an Opportunity Assessment',
 'home_close_cta2': 'Request a Technical Conversation',
 'plat_title': 'The TwoSuns Platform for Cement | Modules, inputs and deployment',
 'plat_desc': "Core and Ray provide the shared foundation. Pulse extends it into the plant, "
               "Horizon into commercial work. Read-only integration throughout.",
 'plat_eyebrow': 'The TwoSuns Platform',
 'plat_h1': 'One enterprise environment. Shared context across the plant and the market.',
 'plat_sub': "TwoSuns connects relevant inputs, organizational context, intelligence, people "
              "and workflows within an adaptive enterprise platform. Core and Ray provide the "
              "common foundation for every deployment. Pulse extends that foundation into the "
              "plant and Horizon into commercial work, within the limits the plant's engineers "
              "own.",
 'plat_cta1': 'Request a Product Demonstration',
 'plat_cta2': 'Request a Technical Conversation',
 'how_tag': 'How it works',
 'how_h': 'Five steps behind every recommendation',
 'how_steps': [
                (
                  'Ingest.',
                  "Historian, laboratory, ERP, cost and market inputs, read from the systems "
                   "already in place.",
                ),
                (
                  'Detect.',
                  "Each value is compared with the band the plant's engineers define and own.",
                ),
                (
                  'Cost.',
                  'Each deviation is costed as exposure per day and ranked by severity.',
                ),
                (
                  'Decide.',
                  'Options go to the people accountable, with the evidence behind them.',
                ),
                (
                  'Record.',
                  "The decision, its owner, its inputs and its outcome stay in the decision "
                   "history.",
                ),
              ],
 'how_carry_h': 'Every decision carries',
 'how_carry': [
                'Deviation against band',
                'Cost exposure per day',
                'Severity',
                'Owner',
                'Approval chain',
                'Disposition',
                'Input lineage',
              ],
 'how_note': 'No one approves their own request.',
 'arch_tag': 'Architecture',
 'arch_h': 'Two operating domains, one shared context',
 'arch_p': "Horizon supports the market-facing work and Pulse supports the plant. Core holds "
            "the context both work from, and Ray works from the context available to each user "
            "and workflow. Activities and results generated in one area can inform related "
            "work elsewhere, while Core maintains continuity.",
 'arch_t1_n': '01',
 'arch_t1_k': 'Administration and inputs',
 'arch_t1_a': 'Restricted access',
 'arch_t1_who': "TwoSuns implementation team and the producer's authorized system "
                 "administrators",
 'arch_t1': [
              'Admin and Security',
              'Integrations',
              'Market Data',
              'DCS Historian and Customer Data',
              'Uploads',
            ],
 'arch_t1_note': "Permitted users contribute through module uploads, defined submissions and "
                  "connected shared drives.",
 'arch_t2_n': '02',
 'arch_t2_k': 'Modules',
 'arch_t2_a': 'Permission-based access',
 'arch_hz_h': 'Horizon',
 'arch_hz_d': 'Commercial coordination',
 'arch_hz_c': '6 modules',
 'arch_hz': [
              'Strategy and Product Market Fit',
              'Omni Signals',
              'Omni Plays',
              'Contracts and Offers',
              'Order Management and Invoicing',
              'Finance',
            ],
 'arch_core_h': 'Core',
 'arch_core_d': 'Shared enterprise context',
 'arch_core': [
                'Organization',
                'Objectives',
                'Business rules',
                'Relationships',
                'Decision history',
              ],
 'arch_pl_h': 'Pulse',
 'arch_pl_d': 'Operational execution',
 'arch_pl_c': '7 modules',
 'arch_pl': [
              'Quarry',
              'Materials and Supply',
              'Crushing and Raw Mix',
              'Pyro Process and Cooling',
              'Grinding and Product',
              'Packing and Dispatch',
              'Sustainability',
            ],
 'arch_t3_n': '03',
 'arch_t3_k': 'Shared facilities',
 'arch_t3_a': 'Permission-based capability',
 'arch_ray': 'Ray, the TwoSuns platform AI agent',
 'arch_t3': [
              'Digital Twin',
              'Optimization and Scenarios',
              'Calendars',
              'Spaces',
              'Dashboards',
              'Inventory',
              'Energy and Resources',
              'Product Quality',
              'Logistics',
            ],
 'arch_t3_note': 'Permissions govern inputs, visibility and actions throughout the platform.',
 'arch_units': "Heat in kcal/kg clinker on an NCV basis. Power in kWh per tonne of cement. "
                "Costs per tonne of clinker or cement, in EGP and US$. CO2 per tonne of "
                "clinker and of cement shown separately.",
 'data_tag': 'Inputs and integration',
 'data_h': 'Bring together the inputs the plant already records',
 'data_p': "A TwoSuns environment can combine internal, external, real-time and human inputs "
            "according to the decision it is configured around.",
 'data_cols': ['Source', 'Typical content', 'Typical frequency'],
 'data_rows': [
                (
                  'Process historian (DCS)',
                  'Kiln, cooler, mill and fan process values',
                  '1 or 5 minute resolution',
                ),
                (
                  'Laboratory and XRF',
                  'Raw meal, hot meal, clinker and cement chemistry; fineness; strength',
                  "Hourly composites for raw mix; about every 4 hours for hot meal; per "
                   "sample for cement",
                ),
                (
                  'Fuel analyses',
                  'NCV as received with analysis date; sulphur, chlorine and ash',
                  'By lot',
                ),
                (
                  'ERP',
                  'Stock, purchase orders, sales orders, ledger',
                  'Hourly or daily extract',
                ),
                ('Weighbridge', 'Tonnes in and out', 'Hourly or by upload'),
                (
                  'Silo levels and surveys',
                  'Radar levels; stockpile and store surveys',
                  'Hourly for radar; surveys as scheduled',
                ),
                ('CEMS and stack tests', 'Dust, SO2, NOx, HCl, HF and TOC', 'Daily averages'),
                (
                  'Market data',
                  'Fuel benchmarks, exchange rates, freight, tenders, competitor activity',
                  'As published, with source and date',
                ),
                (
                  'Uploads',
                  'Spreadsheets, survey sheets, permits and reports',
                  'As submitted by permitted users',
                ),
              ],
 'data_p2': "TwoSuns reads inputs through APIs, configurable connectors, file upload or "
             "direct connection, with templates where a site is not yet connected. Integration "
             "is read-only. Nothing is written to the DCS, PLCs, ERP or laboratory systems, "
             "and the platform works alongside any advanced process control already in "
             "service.",
 'data_p3': "Plant figures are tagged as measured, derived or assumed, and finance figures as "
             "measured, ledger-derived or modelled. Late or stale inputs lower the confidence "
             "shown on the figures that use them.",
 'dep_tag': 'Deployment',
 'dep_h': 'Configure, deploy and expand',
 'dep_steps': [
                (
                  'Conversation.',
                  'The decision that matters most, its owner and the limit that binds.',
                ),
                (
                  'Discovery.',
                  "The plant's inputs are reviewed under a mutual NDA, one decision is "
                   "agreed, and the baseline is measured from the plant's own trailing twelve "
                   "months.",
                ),
                (
                  'Configuration.',
                  "Plant basis, limits, targets and approval chains are set in Core with the "
                   "process, quality and commercial leads.",
                ),
                (
                  'Pilot.',
                  "The relevant modules run read-only on that decision and are measured "
                   "against targets the plant sets.",
                ),
                (
                  'Expansion.',
                  "Further decisions, lines and plants are added once the pilot meets its "
                   "targets.",
                ),
              ],
 'dep_p': "The initial deployment typically takes several weeks to three months, depending on "
           "scope, integrations and operating requirements. The producer decides whether to "
           "continue at the end of each step.",
 'dep_prov_h': 'What the plant provides for discovery',
 'dep_prov': [
               'A trailing twelve months of production and cost reports',
               'The operating limits in force, and the names of the people who own them',
               'A sample of laboratory, XRF and fuel analyses',
               'A stock, order and ledger extract from ERP',
               'The approval chain for the decision in scope, and its named owner',
             ],
 'gov_tag': 'Governance',
 'gov_h': 'Security, access and hosting',
 'gov_rows': [
               (
                 'Permissions by role.',
                 'Permissions govern inputs, visibility and actions throughout the platform.',
               ),
               (
                 'Restricted administration.',
                 "Users, roles and the audit trail are managed by the TwoSuns implementation "
                  "team and the producer's authorized administrators.",
               ),
               (
                 'Audit trail.',
                 'Every recommendation, approval and outcome is logged with its reason.',
               ),
               ('Data isolation.', "Each producer's information is kept separate."),
               (
                 'Hosting.',
                 "A shared managed cloud environment is the preferred option. Dedicated and "
                  "local environments can be evaluated where operating, security, residency or "
                  "performance requirements support a different arrangement. Hosting and data "
                  "residency are agreed before deployment.",
               ),
               (
                 'Confidentiality.',
                 'Documents shared during discovery are covered by a mutual NDA.',
               ),
             ],
 'plat_close_h': 'See the platform on a cement value chain',
 'plat_close_p': "The team can take process, quality, IT and finance leads through the "
                  "modules, the technical basis and the deployment path, from the quarry face "
                  "to cash collected.",
 'ev_title': 'TwoSuns in Cairo | AICCE29 and The Future of Cement',
 'ev_desc': "TwoSuns is in Egypt from 10 to 26 November 2026, at AICCE29 from 23 to 25 "
             "November, with an invitation-only evening for cement leaders on 25 November.",
 'ev_eyebrow': 'Events',
 'ev_h1': 'Meet the TwoSuns team in Cairo.',
 'ev_sub': "The team is in Egypt from 10 to 26 November. It attends AICCE29 from 23 to 25 "
            "November, where Aiman El-Ramly speaks on 24 November, and hosts an "
            "invitation-only evening for cement leaders on 25 November.",
 'ev_cta1': 'Arrange a Meeting',
 'ev_cta2': 'Discuss Your Needs',
 'ev_up_tag': 'Where to find us',
 'ev_up_h': 'Upcoming events',
 'ev_up_p': "Message the team to arrange a meeting at either event, or use the Discuss Your "
             "Needs form.",
 'ev1_when': '23 to 25 November 2026',
 'ev1_where': 'Heliopolis Congress Complex, Waldorf Astoria and Hilton Heliopolis Hotels, Cairo',
 'ev1_h': "AICCE29: 29th Arab International Cement and Building Materials Conference and "
           "Exhibition",
 'ev1_p': "Organized by the Arab Union for Cement and Building Materials (AUCBM). The TwoSuns "
           "team attends all three days and can meet during the conference.",
 'ev1_cta': 'Arrange a Meeting at AICCE29',
 'ses_tag': 'Speaker session',
 'ses_day': '24',
 'ses_mon': 'Nov',
 'ses_code': 'Session 10.7',
 'ses_h': 'Understanding the Domain and Impact of AI in Heavy Industry',
 'ses_who': 'Aiman El-Ramly, Chief Executive Officer, TwoSuns',
 'ses_p': "A session on where AI applies across heavy industry operations, and how it affects "
           "cost, output and commercial performance for producers.",
 'ses_when': 'Tuesday, 24 November 2026',
 'ses_time': '13:30 to 13:45',
 'ses_place': 'Heliopolis Congress Complex, Cairo',
 'ev2_badge': 'By invitation only · Hosted by TwoSuns with the Korayem Group',
 'ev2_h': 'The Future of Cement: Transformation and Innovation',
 'ev2_kicker': 'An exclusive evening reception',
 'ev2_line': 'Innovation and the future of cement, from North America to the Middle East',
 'ev2_when': 'Wednesday, 25 November 2026',
 'ev2_time': '16:00 to 23:00',
 'ev2_place': 'Sky Executive Resort, New Cairo',
 'ev2_dress': 'Business attire',
 'ev2_p': "An invitation-only evening for cement producers in Egypt. The programme includes "
           "short talks on AI, digital twins and research in heavy industry, a panel of cement "
           "leaders on operations and decision-making, and a live demonstration of the TwoSuns "
           "Platform across one cement value chain, from the quarry face to cash collected. "
           "Dinner and networking follow.",
 'ev2_cta1': 'Register Your Place',
 'ev2_cta2': 'Request an Invitation',
 'ev2_note': 'Use the access code in your invitation to register. Places are limited.',
 'ag_h': 'Evening agenda',
 'ag_rows': [
              (
                '16:00 to 18:00',
                'Reception and Registration',
                '',
                'Welcome refreshments, registration and networking',
                [],
              ),
              (
                '18:00 to 18:15',
                'Welcome and Intent',
                '',
                'Opening remarks and the intent for the evening',
                [
                  'Aiman El-Ramly, Chief Executive Officer, TwoSuns',
                  'Dr. Ahmed Shireen Korayem, Korayem Group',
                ],
              ),
              (
                '18:15 to 18:30',
                'Understanding AI and Digital Transformation',
                'Talk',
                'What the shift means for heavy industry, and where it starts',
                ['Ryan Arian, Chief Digital Product Officer, TwoSuns'],
              ),
              (
                '18:30 to 18:45',
                'Digital Twins in Heavy Industry',
                'Talk',
                'From the 3D model of the quarry face to everyday operating decisions',
                ['A senior executive from a heavy-industry producer, to be announced'],
              ),
              (
                '18:45 to 19:00',
                'The Research View',
                'Talk',
                'AI and digital transformation in industry',
                ['A university researcher, to be announced'],
              ),
              ('19:00 to 19:30', 'Break and Networking', '', '', []),
              (
                '19:30 to 20:10',
                'Panel: From the Plant to the Boardroom',
                'Panel',
                'AI and operational excellence in cement',
                ['Aiman El-Ramly, TwoSuns', 'With cement industry leaders, to be announced'],
              ),
              (
                '20:10 to 20:25',
                'TwoSuns Platform Overview',
                '',
                'The team behind TwoSuns and how the platform is structured',
                ['TwoSuns team'],
              ),
              (
                '20:25 to 21:00',
                'Live Demonstration: Quarry to Cash',
                'Live demo',
                "The TwoSuns Platform across one cement value chain, from the quarry face to "
                 "cash collected",
                ['TwoSuns team'],
              ),
              (
                '21:00 to 21:15',
                'Q&A and Closing',
                '',
                'Questions to the speakers, then closing remarks',
                ['Aiman El-Ramly, TwoSuns'],
              ),
              (
                '21:15 to 22:15',
                'Dinner',
                '',
                "Bring a challenge from your own plant to the TwoSuns desk for a one-to-one "
                 "platform session",
                [],
              ),
              ('22:15 to 23:00', 'Networking', '', '', []),
            ],
 'ag_note': 'Speakers are being confirmed and will be added here.',
 'pd_tag': 'Practical details',
 'pd_rows': [
              ('Date', 'Wednesday, 25 November 2026'),
              ('Time', '16:00 to 23:00'),
              ('Venue', 'Sky Executive Resort, New Cairo'),
              ('Dress code', 'Business attire'),
              ('Entry', 'By invitation, registration required'),
              ('Getting there', 'Directions come with your confirmation.'),
              ('Photography', 'Photos and video will be taken during the evening.'),
              ('Questions', 'info@twosuns.ai or WhatsApp +1 250 859 6563'),
            ],
 'past_tag': 'Already happened',
 'past_h': 'Where we have been',
 'past_p': 'If we met at one of these events, the team can continue the conversation.',
 'past_rows': [
                (
                  'Egypt Mining Forum 2026',
                  '28 to 29 September 2026',
                  'The St. Regis New Capital, Cairo',
                ),
                (
                  'INTERCEM 2026',
                  '8 to 10 September 2026',
                  'Swissotel The Bosphorus, Istanbul, Turkiye',
                ),
                (
                  'Egypt Projects 2026',
                  '5 to 7 September 2026',
                  'Egypt International Exhibition Center, Cairo',
                ),
              ],
 'ev_close_h': 'Not attending one of these?',
 'ev_close_p': "Share what you want to look at, and the team will arrange a meeting in Cairo "
                "or a call.",
 'menu_label': 'Menu',
 'table_label': 'Inputs and integration, scrollable table',
}


AR = {
 'lang': 'ar',
 'dir': 'rtl',
 'other': 'en',
 'other_label': 'EN',
 'self_label': 'العربية',
 'nav': [
          ('نبذة عنا', 'index.html#about'),
          ('سياق صناعة الأسمنت', 'index.html#context'),
          ('المنصة', 'platform.html'),
          ('الفعاليات', 'events.html'),
        ],
 'nav_cta': 'ناقش احتياجاتك',
 'skip': 'انتقل إلى المحتوى',
 'by': 'TwoSuns من AEPG',
 'foot_links': [
                 ('نبذة عنا', 'index.html#about'),
                 ('سياق صناعة الأسمنت', 'index.html#context'),
                 ('المنصة', 'platform.html'),
                 ('الفعاليات', 'events.html'),
                 ('ناقش احتياجاتك', 'https://twosuns.ai/discuss.html'),
               ],
 'foot_email': 'info@twosuns.ai',
 'foot_wa': 'واتساب +1 250 859 6563',
 'foot_rights': '© 2026 TwoSuns من AEPG. جميع الحقوق محفوظة.',
 'foot_privacy': 'الخصوصية',
 'foot_terms': 'الشروط',
 'main_site': 'twosuns.ai',
 'home_title': 'TwoSuns لصناعة الأسمنت | سياق مؤسسي مشترك من المحجر إلى التحصيل',
 'home_desc': "منصة مؤسسية متكيفة مُهيّأة وفق صناعة الأسمنت. تُنسّق TwoSuns قرارات المحجر "
               "والفرن والطاحونة والشحن والمبيعات عبر سياق مؤسسي مشترك، داخل الحدود التي "
               "يملكها مهندسو المصنع.",
 'home_eyebrow': 'قدرة مؤسسية متكيفة لمنتجي الأسمنت',
 'home_h1': 'تنمية الأعمال المركبة وتشغيلها وتنسيقها عبر سياق مؤسسي مشترك.',
 'home_sub': "TwoSuns منصة مؤسسية متكيفة لقطاع البناء والأصول المبنية، مُهيّأة هنا وفق صناعة "
              "الأسمنت. تجمع المنصة المدخلات التي يسجلها المصنع بالفعل، والذكاء المدرك للسياق، "
              "ودعمًا من وكلاء أذكياء، ومسارات عمل قابلة للتهيئة، بحيث تنسّق فرق العمليات "
              "والجودة والنشاط التجاري والمالية من السياق نفسه.",
 'home_cta1': 'ناقش احتياجاتك',
 'home_cta2': 'استعرض المنصة',
 'about_tag': 'نبذة عن TwoSuns',
 'about_h': 'خبرة مؤسسية مطبّقة على عمل منتج الأسمنت',
 'about_p1': "تجمع TwoSuns بين الاستراتيجية المؤسسية وقيادة المنتج والمعرفة القطاعية وخبرة "
              "النمو والتحليلات وهندسة البرمجيات والذكاء الاصطناعي وهندسة البيانات وقدرة "
              "التنفيذ. تُطوّر AEPG المنصة في كندا، وتُهيّأ مع مسؤولي العمليات والجودة والنشاط "
              "التجاري لدى المنتج نفسه.",
 'about_p2': "نبني قدرة مؤسسية عملية تساعد المنشآت على النمو والتشغيل وتنسيق الأعمال المركبة "
              "عبر سياق مترابط وذكاء ومسارات عمل قابلة للتهيئة. وفي صناعة الأسمنت يمتد هذا "
              "العمل من واجهة المحجر إلى النقد المحصّل، وتنفّذه وظائف تحتفظ كل واحدة منها "
              "بسلطتها.",
 'about_fam_h': 'منصة واحدة تغطي المصنع والسوق',
 'fams': [
           (
             'Core',
             'طبقة السياق المؤسسي المشترك والتهيئة والاستمرارية.',
             'أساس المصنع، وحدود التشغيل، والأدوار، وسلاسل الموافقات، وسجل القرارات.',
           ),
           (
             'Ray',
             'مساعدة مدركة للسياق متاحة في كل أنحاء المنصة.',
             'شرح وتركيب ودعم لمسارات العمل، داخل صلاحيات كل مستخدم.',
           ),
           (
             'Horizon',
             'قدرات السوق والنمو والعلاقات والنشاط التجاري.',
             "الاستراتيجية وملاءمة المنتج للسوق، والمؤشرات، والخطط، والعقود والعروض، وإدارة "
              "الطلبات والفوترة، والمالية.",
           ),
           (
             'Pulse',
             'قدرات المنتج والمشروعات والتشغيل والأصول.',
             "المحجر، والمواد والتوريد، والخلطة الخام، والعملية الحرارية، والطحن، والتعبئة "
              "والشحن، والاستدامة.",
           ),
         ],
 # the platform architecture figure on the home page, drawn by arch.py
 'arx_tag': 'البنية',
 'arx_h': 'يتحول السياق المؤسسي إلى إجراء منسّق',
 'arx_p': 'الذكاء التجاري والتنفيذ التشغيلي مترابطان عبر سياق مؤسسي واحد خاضع للضوابط.',
 'arx_foot': 'سياق واحد خاضع للضوابط. مجالا تشغيل. إدراك مؤسسي مستمر.',
 'arx_cta': 'استعرض المنصة',
 'arx_labels': {
                 'core_1': 'الضوابط والصلاحيات',
                 'core_2': 'الذاكرة التنظيمية والسجلات',
                 'core_3': 'استمرارية القرارات',
                 'core_k': 'السياق الخاضع للضوابط',
                 'flow_in': 'سياق وارد',
                 'flow_out': 'إجراء منسّق صادر',
                 'hz_1': 'ذكاء السوق والعملاء',
                 'hz_2': 'تنسيق الإيرادات',
                 'hz_3': 'التنفيذ الموجّه للسوق',
                 'hz_k': 'الذكاء التجاري',
                 'orb_customers': 'العملاء',
                 'orb_markets': 'الأسواق',
                 'orb_operations': 'العمليات',
                 'orb_people': 'الأشخاص والأنظمة',
                 'pl_1': 'مسارات العمل التشغيلية',
                 'pl_2': 'تنسيق التوريد والموارد',
                 'pl_3': 'إدارة الأداء',
                 'pl_k': 'التنفيذ التشغيلي',
                 'ray_1': 'استمرارية السياق',
                 'ray_2': 'الإدراك المؤسسي',
                 'ray_3': 'الإجراء المنسّق',
                 'ray_sub': 'مساعد مؤسسي دائم الحضور',
                 'svg_aria': 'Horizon وPulse مجالا تشغيل، وCore هو السياق الخاضع للضوابط بينهما، وRay يمتد تحتهما.',
               },
 'ctx_tag': 'سياق صناعة الأسمنت',
 'ctx_h': 'تكلفة الطن تتحدد بقرارات تُتخذ في وظائف منفصلة',
 'ctx_p1': "يتخذ مصنع الأسمنت كل يوم قرارات كثيرة تحرك تكلفة الطن: أي واجهات المحجر تغذي "
            "الكسّارة، وكيف تُصحّح الخلطة الخام، وأي أنواع الوقود تُحرق، وأي الصوامع تُفرّغ، "
            "وأي الأطنان والأسعار تلتزم بها المبيعات. وكل قرار منها يقع في وظيفة مختلفة ونظام "
            "مختلف.",
 'ctx_p2': "تجمع TwoSuns هذه القرارات في بيئة مؤسسية واحدة إلى جانب الأنظمة القائمة بالفعل. "
            "تحتفظ كل وظيفة بسلطتها وترى أثر قرارها على التكلفة والطاقة الإنتاجية والمخزون "
            "والجودة في باقي أجزاء الأعمال.",
 'ctx_cond_h': 'ظروف مشتركة في تشغيل الأسمنت',
 'ctx_cond': [
               'دورات حياة طويلة للمحجر والفرن والأصول',
               'وظائف عديدة تشارك في إنتاج الطن الواحد',
               'متطلبات إقليمية وتراخيص وممارسات تشغيل',
               'علاقات تجارية وفنية وتنظيمية مركبة',
               'مدخلات مادية ومالية وسوقية وتشغيلية',
               'تناقل متكرر للمسؤولية عبر حدود الوظائف',
               'قيمة مستمرة بعد إنتاج الطن بزمن طويل',
             ],
 'ctx_flow_h': 'تتبّع مسار العمل عبر المصنع',
 'ctx_flow_p': "تغيير عند واجهة المحجر يحرك تصحيح الخلطة الخام، وحرارة الفرن، وجودة الكلنكر، "
                "ومقاومة الأسمنت، والأطنان التي يمكن للشحن تسليمها، والأسعار التي يمكن "
                "للمبيعات الالتزام بها. وأمر تصدير يُقبل يوم الاثنين يحدد قرارات الطحن "
                "والتعبئة والمخزون لباقي الأسبوع. أعمال الأسمنت مترابطة عبر مسارات العمل "
                "المستمرة هذه، والمنصة تُهيّأ حولها.",
 'cfg_tag': 'التهيئة',
 'cfg_h': 'هيّئ TwoSuns وفق مصنعك',
 'cfg_p': "المصانع التي تتشابه أفرانها قد تحتاج قرارات مختلفة في اليوم نفسه. يُشكّل كل تطبيق "
           "حول أساس المصنع نفسه، وبيئته التشغيلية، ومستخدميه، ومناطقه، ومدخلاته، وتكاملاته، "
           "والقيمة المتوقعة، ويُهيّأ مع مسؤولي العمليات والجودة والنشاط التجاري قبل أن تنتج "
           "المنصة أي توصية.",
 'cfg_rows': [
               (
                 'المصنع والخطوط',
                 'خطوط الأفران والطواحين وماكينات التعبئة والصوامع، مع حدود تشغيلها',
               ),
               (
                 'المواد الخام والوقود',
                 "كيمياء المحجر والمواد المصححة، والوقود بقيمته الحرارية ونسب الكبريت والكلور "
                  "والرماد",
               ),
               (
                 'المواصفات والتراخيص',
                 "رتب الأسمنت المنتجة، وتراخيص المداخن، وتراخيص الوقود، وتقارير التصدير "
                  "والكربون",
               ),
               (
                 'التنظيم والموافقات',
                 'الأدوار والتسلسل الإداري وسلاسل الموافقات ومستويات الصلاحية',
               ),
               ('الأسواق', 'المناطق والقنوات والعملاء وجهات التصدير'),
               (
                 'المدخلات',
                 "قاعدة البيانات التاريخية والمختبر ونظام ERP وميزان القبّان والمسوحات، ومعدل "
                  "ورود كل منها",
               ),
             ],
 'home_close_h': 'ابدأ بالقرار الأكثر أهمية الآن',
 'home_close_p': "تُطور TwoSuns في كندا. الفريق في القاهرة من 10 إلى 26 نوفمبر، ويمكنه اللقاء "
                  "في مصنعك أو مكتبك لمراجعة قرار واحد في ضوء تقاريرك أنت، بموجب اتفاقية سرية "
                  "متبادلة.",
 'home_close_cta1': 'اطلب تقييم فرصة',
 'home_close_cta2': 'اطلب محادثة فنية',
 'plat_title': 'منصة TwoSuns للأسمنت | الوحدات والمدخلات والتطبيق',
 'plat_desc': "يوفر Core وRay الأساس المشترك. يمتد Pulse إلى المصنع وHorizon إلى النشاط "
               "التجاري. تكامل للقراءة فقط مع مدخلات النظام التاريخي والمختبر وERP وميزان "
               "القبّان.",
 'plat_eyebrow': 'منصة TwoSuns',
 'plat_h1': 'بيئة مؤسسية واحدة. سياق مشترك يربط المصنع بالسوق.',
 'plat_sub': "تربط TwoSuns المدخلات المعنية والسياق التنظيمي والذكاء والأشخاص ومسارات العمل "
              "داخل منصة مؤسسية متكيفة. يوفر Core وRay الأساس المشترك لكل تطبيق. ويمتد Pulse "
              "بهذا الأساس إلى المصنع وHorizon إلى النشاط التجاري، داخل الحدود التي يملكها "
              "مهندسو المصنع.",
 'plat_cta1': 'اطلب عرضًا توضيحيًا للمنتج',
 'plat_cta2': 'اطلب محادثة فنية',
 'how_tag': 'كيف تعمل',
 'how_h': 'خمس خطوات وراء كل توصية',
 'how_steps': [
                (
                  'الاستيعاب.',
                  "مدخلات النظام التاريخي والمختبر وERP والتكلفة والسوق، تُقرأ من الأنظمة "
                   "القائمة بالفعل.",
                ),
                ('الاكتشاف.', 'تُقارن كل قيمة بالنطاق الذي يحدده ويملكه مهندسو المصنع.'),
                ('التكلفة.', 'يُقاس كل انحراف كتعرّض مالي يومي ويُرتب بحسب درجة الخطورة.'),
                ('القرار.', 'تُعرض الخيارات على المسؤولين، مع الأدلة التي تستند إليها.'),
                ('التسجيل.', 'يبقى القرار ومسؤوله ومدخلاته ونتيجته في سجل القرارات.'),
              ],
 'how_carry_h': 'كل قرار يحمل',
 'how_carry': [
                'الانحراف عن النطاق',
                'التعرّض المالي اليومي',
                'درجة الخطورة',
                'المسؤول',
                'سلسلة الموافقات',
                'التصرف النهائي',
                'مسار المدخلات',
              ],
 'how_note': 'لا أحد يوافق على طلبه الخاص.',
 'arch_tag': 'البنية',
 'arch_h': 'مجالا تشغيل، وسياق مشترك واحد',
 'arch_p': "يدعم Horizon العمل الموجّه للسوق ويدعم Pulse المصنع. يحمل Core السياق الذي يعمل "
            "منه كلاهما، ويعمل Ray من السياق المتاح لكل مستخدم ومسار عمل. والأنشطة والنتائج "
            "المتحققة في مجال واحد يمكن أن يُسترشَد بها في أعمال ذات صلة في مواضع أخرى، بينما "
            "يحفظ Core الاستمرارية.",
 'arch_t1_n': '01',
 'arch_t1_k': 'الإدارة والمدخلات',
 'arch_t1_a': 'وصول مقيّد',
 'arch_t1_who': 'فريق تنفيذ TwoSuns ومديرو النظام المعتمدون لدى المنتج',
 'arch_t1': [
              'الإدارة والأمن',
              'التكاملات',
              'بيانات السوق',
              'النظام التاريخي DCS وبيانات العملاء',
              'الملفات المُحمّلة',
            ],
 'arch_t1_note': "يساهم المستخدمون المسموح لهم عبر ملفات تُحمّل في الوحدات، ونماذج محددة، "
                  "وأقراص مشتركة متصلة.",
 'arch_t2_n': '02',
 'arch_t2_k': 'الوحدات',
 'arch_t2_a': 'وصول قائم على الصلاحيات',
 'arch_hz_h': 'Horizon',
 'arch_hz_d': 'التنسيق التجاري',
 'arch_hz_c': '6 وحدات',
 'arch_hz': [
              'الاستراتيجية وملاءمة المنتج للسوق',
              'Omni Signals',
              'Omni Plays',
              'العقود والعروض',
              'إدارة الطلبات والفوترة',
              'المالية',
            ],
 'arch_core_h': 'Core',
 'arch_core_d': 'السياق المؤسسي المشترك',
 'arch_core': ['التنظيم', 'الأهداف', 'قواعد العمل', 'العلاقات', 'سجل القرارات'],
 'arch_pl_h': 'Pulse',
 'arch_pl_d': 'التنفيذ التشغيلي',
 'arch_pl_c': '7 وحدات',
 'arch_pl': [
              'المحجر',
              'المواد والتوريد',
              'التكسير والخلطة الخام',
              'العملية الحرارية والتبريد',
              'الطحن والمنتج',
              'التعبئة والشحن',
              'الاستدامة',
            ],
 'arch_t3_n': '03',
 'arch_t3_k': 'المرافق المشتركة',
 'arch_t3_a': 'قدرات قائمة على الصلاحيات',
 'arch_ray': 'Ray، الوكيل الذكي لمنصة TwoSuns',
 'arch_t3': [
              'التوأم الرقمي',
              'التحسين والسيناريوهات',
              'التقاويم',
              'المساحات',
              'لوحات المتابعة',
              'المخزون',
              'الطاقة والموارد',
              'جودة المنتج',
              'الخدمات اللوجستية',
            ],
 'arch_t3_note': 'تحكم الصلاحيات المدخلات والرؤية والإجراءات في كل أنحاء المنصة.',
 'arch_units': "الحرارة بوحدة kcal/kg كلنكر على أساس NCV. الطاقة بوحدة kWh لكل طن أسمنت. "
                "التكاليف لكل طن كلنكر أو أسمنت، بالجنيه المصري والدولار الأمريكي. ويُعرض ثاني "
                "أكسيد الكربون لكل طن كلنكر ولكل طن أسمنت كلٌّ على حدة.",
 'data_tag': 'المدخلات والتكامل',
 'data_h': 'اجمع المدخلات التي يسجلها المصنع بالفعل',
 'data_p': "يمكن لبيئة TwoSuns أن تجمع مدخلات داخلية وخارجية وفورية وبشرية بحسب القرار الذي "
            "تُهيّأ حوله.",
 'data_cols': ['المصدر', 'المحتوى المعتاد', 'التكرار المعتاد'],
 'data_rows': [
                (
                  'النظام التاريخي للعملية (DCS)',
                  'قيم تشغيل الفرن والمبرد والطاحونة والمراوح',
                  'بدقة دقيقة واحدة أو 5 دقائق',
                ),
                (
                  'المختبر وتحليل XRF',
                  'كيمياء الوجبة الخام والوجبة الساخنة والكلنكر والأسمنت؛ النعومة؛ المقاومة',
                  'مجمعات كل ساعة للخلطة الخام؛ نحو كل 4 ساعات للوجبة الساخنة؛ لكل عينة أسمنت',
                ),
                (
                  'تحليلات الوقود',
                  "القيمة الحرارية الصافية على أساس الاستلام مع تاريخ التحليل؛ الكبريت "
                   "والكلور والرماد",
                  'لكل دفعة',
                ),
                (
                  'ERP',
                  'المخزون وأوامر الشراء وأوامر البيع ودفتر الأستاذ',
                  'استخراج كل ساعة أو كل يوم',
                ),
                ('ميزان القبّان', 'الأطنان الداخلة والخارجة', 'كل ساعة أو برفع ملف'),
                (
                  'مناسيب الصوامع والمسوحات',
                  'مناسيب الرادار؛ مسوحات المخازن والأكوام',
                  'كل ساعة للرادار؛ والمسوحات بحسب الجدول',
                ),
                (
                  'القياس المستمر للانبعاثات واختبارات المداخن',
                  'الغبار وSO2 وNOx وHCl وHF وTOC',
                  'متوسطات يومية',
                ),
                (
                  'بيانات السوق',
                  'مراجع أسعار الوقود وأسعار الصرف والشحن والمناقصات ونشاط المنافسين',
                  'كما تُنشر، مع المصدر والتاريخ',
                ),
                (
                  'الملفات المُحمّلة',
                  'جداول بيانات وأوراق مسح وتراخيص وتقارير',
                  'بحسب ما يقدمه المستخدمون المسموح لهم',
                ),
              ],
 'data_p2': "تقرأ TwoSuns المدخلات عبر واجهات برمجية وموصلات قابلة للتهيئة وتحميل ملفات أو "
             "اتصال مباشر، مع نماذج جاهزة حيث لا يكون الموقع متصلًا بعد. التكامل للقراءة فقط. "
             "لا يُكتب شيء إلى أنظمة DCS أو PLC أو ERP أو المختبر، وتعمل المنصة جنبًا إلى جنب "
             "مع أي نظام تحكم متقدم قيد الخدمة.",
 'data_p3': "تُوسم أرقام المصنع بأنها مقاسة أو مستنتجة أو مفترضة، وأرقام المالية بأنها مقاسة "
             "أو مستندة إلى الدفاتر أو مُنمذَجة. والمدخلات المتأخرة أو القديمة تخفض درجة الثقة "
             "المعروضة على الأرقام التي تستخدمها.",
 'dep_tag': 'التطبيق',
 'dep_h': 'التهيئة والتطبيق والتوسع',
 'dep_steps': [
                ('المحادثة.', 'القرار الأكثر أهمية، ومسؤوله، والحد الملزم.'),
                (
                  'الاستكشاف.',
                  "تُراجع مدخلات المصنع بموجب اتفاقية سرية متبادلة، ويُتفق على قرار واحد، "
                   "ويُقاس خط الأساس من تقارير المصنع نفسه عن الأشهر الاثني عشر الماضية.",
                ),
                (
                  'التهيئة.',
                  "تُحدد أساس المصنع والحدود والأهداف وسلاسل الموافقات في Core مع مسؤولي "
                   "العمليات والجودة والنشاط التجاري.",
                ),
                (
                  'التشغيل التجريبي.',
                  "تعمل الوحدات المعنية للقراءة فقط على هذا القرار، وتُقاس بالمقارنة بأهداف "
                   "يضعها المصنع.",
                ),
                (
                  'التوسع.',
                  'تُضاف قرارات وخطوط ومصانع أخرى بعد أن يحقق التشغيل التجريبي أهدافه.',
                ),
              ],
 'dep_p': "يستغرق التطبيق الأولي عادة من عدة أسابيع إلى ثلاثة أشهر، بحسب النطاق والتكاملات "
           "ومتطلبات التشغيل. والمنتج هو من يقرر الاستمرار من عدمه في نهاية كل خطوة.",
 'dep_prov_h': 'ما يوفره المصنع لمرحلة الاستكشاف',
 'dep_prov': [
               'تقارير الإنتاج والتكلفة لاثني عشر شهرًا سابقة',
               'حدود التشغيل السارية، وأسماء من يملكونها',
               'عينة من تحليلات المختبر وXRF والوقود',
               'استخراج للمخزون والطلبات والدفاتر من ERP',
               'سلسلة الموافقات للقرار المعني، ومسؤوله المحدد',
             ],
 'gov_tag': 'الضوابط',
 'gov_h': 'الأمن والوصول والاستضافة',
 'gov_rows': [
               (
                 'الصلاحيات بحسب الدور.',
                 'تحكم الصلاحيات المدخلات والرؤية والإجراءات في كل أنحاء المنصة.',
               ),
               (
                 'إدارة مقيّدة.',
                 "يدير المستخدمين والأدوار وسجل التدقيق فريق تنفيذ TwoSuns والمديرون "
                  "المعتمدون لدى المنتج.",
               ),
               ('سجل التدقيق.', 'تُسجل كل توصية وموافقة ونتيجة مع سببها.'),
               ('عزل البيانات.', 'تُحفظ معلومات كل شركة منتِجة على حدة.'),
               (
                 'الاستضافة.',
                 "الخيار المفضل هو بيئة سحابية مشتركة مدارة. ويمكن دراسة بيئات مخصصة أو محلية "
                  "حيث تدعم متطلبات التشغيل أو الأمن أو موقع البيانات أو الأداء ترتيبًا "
                  "مختلفًا. ويُتفق على الاستضافة وموقع البيانات قبل التطبيق.",
               ),
               (
                 'السرية.',
                 'المستندات التي تُتبادل خلال الاستكشاف مشمولة باتفاقية سرية متبادلة.',
               ),
             ],
 'plat_close_h': 'شاهد المنصة على سلسلة قيمة أسمنت',
 'plat_close_p': "يمكن للفريق أن يأخذ مسؤولي العمليات والجودة وتقنية المعلومات والمالية في "
                  "جولة عبر الوحدات والأساس الفني ومسار التطبيق، من واجهة المحجر إلى النقد "
                  "المحصّل.",
 'ev_title': 'TwoSuns في القاهرة | AICCE29 ومستقبل الأسمنت',
 'ev_desc': "فريق TwoSuns في مصر من 10 إلى 26 نوفمبر 2026. يحضر الفريق AICCE29 من 23 إلى 25 "
             "نوفمبر، ويتحدث يوم 24 نوفمبر، ويستضيف أمسية بالدعوة فقط لقادة الأسمنت يوم 25 "
             "نوفمبر.",
 'ev_eyebrow': 'الفعاليات',
 'ev_h1': 'التقِ بفريق TwoSuns في القاهرة.',
 'ev_sub': "الفريق في مصر من 10 إلى 26 نوفمبر. يحضر AICCE29 من 23 إلى 25 نوفمبر، حيث يتحدث "
            "أيمن الرملي يوم 24 نوفمبر، ويستضيف أمسية بالدعوة فقط لقادة الأسمنت يوم 25 نوفمبر.",
 'ev_cta1': 'رتّب لقاءً',
 'ev_cta2': 'ناقش احتياجاتك',
 'ev_up_tag': 'أين تجدنا',
 'ev_up_h': 'الفعاليات القادمة',
 'ev_up_p': 'راسل الفريق لترتيب لقاء في أي من الفعاليتين، أو استخدم نموذج ناقش احتياجاتك.',
 'ev1_when': '23 إلى 25 نوفمبر 2026',
 'ev1_where': 'مجمع مؤتمرات مصر الجديدة، وفندقا والدورف أستوريا وهيلتون مصر الجديدة، القاهرة',
 'ev1_h': 'AICCE29: المؤتمر والمعرض العربي الدولي التاسع والعشرون للأسمنت ومواد البناء',
 'ev1_p': "ينظمه الاتحاد العربي للأسمنت ومواد البناء (AUCBM). يحضر فريق TwoSuns الأيام "
           "الثلاثة كلها ويمكنه اللقاء خلال المؤتمر.",
 'ev1_cta': 'رتّب لقاءً في AICCE29',
 'ses_tag': 'جلسة متحدث',
 'ses_day': '24',
 'ses_mon': 'نوفمبر',
 'ses_code': 'الجلسة 10.7',
 'ses_h': 'فهم مجال الذكاء الاصطناعي وأثره في الصناعة الثقيلة',
 'ses_who': 'أيمن الرملي، الرئيس التنفيذي، TwoSuns',
 'ses_p': "جلسة عن مواضع تطبيق الذكاء الاصطناعي في عمليات الصناعة الثقيلة، وكيف يؤثر على "
           "التكلفة والإنتاج والأداء التجاري للمنتجين.",
 'ses_when': 'الثلاثاء 24 نوفمبر 2026',
 'ses_time': '13:30 إلى 13:45',
 'ses_place': 'مجمع مؤتمرات مصر الجديدة، القاهرة',
 'ev2_badge': 'بالدعوة فقط · تستضيفها TwoSuns مع مجموعة قرايم',
 'ev2_h': 'مستقبل الأسمنت: التحول والابتكار',
 'ev2_kicker': 'حفل استقبال مسائي حصري',
 'ev2_line': 'الابتكار ومستقبل الأسمنت، من أمريكا الشمالية إلى الشرق الأوسط',
 'ev2_when': 'الأربعاء 25 نوفمبر 2026',
 'ev2_time': '16:00 إلى 23:00',
 'ev2_place': 'منتجع سكاي إكزكيوتيف، القاهرة الجديدة',
 'ev2_dress': 'الزي الرسمي',
 'ev2_p': "أمسية بالدعوة فقط لمنتجي الأسمنت في مصر. يشمل البرنامج كلمات قصيرة عن الذكاء "
           "الاصطناعي والتوائم الرقمية والبحث في الصناعة الثقيلة، وجلسة نقاش لقادة الأسمنت حول "
           "العمليات واتخاذ القرار، وعرضًا حيًا لمنصة TwoSuns على سلسلة قيمة أسمنت واحدة، من "
           "واجهة المحجر إلى النقد المحصّل. يتبع ذلك العشاء والتواصل.",
 'ev2_cta1': 'احجز مقعدك',
 'ev2_cta2': 'اطلب دعوة',
 'ev2_note': 'استخدم رمز الدخول الوارد في دعوتك للتسجيل. المقاعد محدودة.',
 'ag_h': 'برنامج الأمسية',
 'ag_rows': [
              ('16:00 إلى 18:00', 'الاستقبال والتسجيل', '', 'مرطبات ترحيبية وتسجيل وتواصل', []),
              (
                '18:00 إلى 18:15',
                'الترحيب والمقصد',
                '',
                'كلمة افتتاحية ومقصد الأمسية',
                ['أيمن الرملي، الرئيس التنفيذي، TwoSuns', 'د. أحمد شيرين قرايم، مجموعة قرايم'],
              ),
              (
                '18:15 إلى 18:30',
                'فهم الذكاء الاصطناعي والتحول الرقمي',
                'كلمة',
                'ما يعنيه هذا التحول للصناعة الثقيلة، ومن أين يبدأ',
                ['رايان أريان، المدير التنفيذي للمنتج الرقمي، TwoSuns'],
              ),
              (
                '18:30 إلى 18:45',
                'التوائم الرقمية في الصناعة الثقيلة',
                'كلمة',
                'من النموذج الثلاثي الأبعاد لواجهة المحجر إلى قرارات التشغيل اليومية',
                ['أحد كبار التنفيذيين في منشأة صناعة ثقيلة، يُعلن عنه لاحقًا'],
              ),
              (
                '18:45 إلى 19:00',
                'المنظور البحثي',
                'كلمة',
                'الذكاء الاصطناعي والتحول الرقمي في الصناعة',
                ['باحث جامعي، يُعلن عنه لاحقًا'],
              ),
              ('19:00 إلى 19:30', 'استراحة وتواصل', '', '', []),
              (
                '19:30 إلى 20:10',
                'جلسة نقاش: من المصنع إلى مجلس الإدارة',
                'نقاش',
                'الذكاء الاصطناعي والتميز التشغيلي في الأسمنت',
                ['أيمن الرملي، TwoSuns', 'مع قادة من صناعة الأسمنت، يُعلن عنهم لاحقًا'],
              ),
              (
                '20:10 إلى 20:25',
                'نظرة عامة على منصة TwoSuns',
                '',
                'الفريق وراء TwoSuns وكيف تُبنى المنصة',
                ['فريق TwoSuns'],
              ),
              (
                '20:25 إلى 21:00',
                'عرض حي: من المحجر إلى التحصيل',
                'عرض حي',
                'منصة TwoSuns على سلسلة قيمة أسمنت واحدة، من واجهة المحجر إلى النقد المحصّل',
                ['فريق TwoSuns'],
              ),
              (
                '21:00 إلى 21:15',
                'أسئلة وختام',
                '',
                'أسئلة للمتحدثين، ثم كلمة ختامية',
                ['أيمن الرملي، TwoSuns'],
              ),
              (
                '21:15 إلى 22:15',
                'العشاء',
                '',
                'أحضر تحديًا من مصنعك إلى طاولة TwoSuns لجلسة فردية حول المنصة',
                [],
              ),
              ('22:15 إلى 23:00', 'التواصل', '', '', []),
            ],
 'ag_note': 'جارٍ تأكيد المتحدثين وستُضاف أسماؤهم هنا.',
 'pd_tag': 'تفاصيل عملية',
 'pd_rows': [
              ('التاريخ', 'الأربعاء 25 نوفمبر 2026'),
              ('الوقت', '16:00 إلى 23:00'),
              ('المكان', 'منتجع سكاي إكزكيوتيف، القاهرة الجديدة'),
              ('الزي', 'الزي الرسمي'),
              ('الدخول', 'بالدعوة، والتسجيل مطلوب'),
              ('الوصول', 'ترد إرشادات الوصول مع تأكيد حجزك.'),
              ('التصوير', 'سيتم التصوير الفوتوغرافي والفيديو خلال الأمسية.'),
              ('الاستفسارات', 'info@twosuns.ai أو واتساب +1 250 859 6563'),
            ],
 'past_tag': 'ما مضى',
 'past_h': 'أين كنا',
 'past_p': 'إن كنا قد التقينا في إحدى هذه الفعاليات، يمكن للفريق متابعة الحديث.',
 'past_rows': [
                (
                  'منتدى مصر للتعدين 2026',
                  '28 إلى 29 سبتمبر 2026',
                  'فندق سنت ريجيس، العاصمة الإدارية الجديدة، القاهرة',
                ),
                (
                  'INTERCEM 2026',
                  '8 إلى 10 سبتمبر 2026',
                  'فندق سويس أوتيل البوسفور، إسطنبول، تركيا',
                ),
                (
                  'Egypt Projects 2026',
                  '5 إلى 7 سبتمبر 2026',
                  'مركز مصر للمعارض الدولية، القاهرة',
                ),
              ],
 'ev_close_h': 'ألا تحضر أيًّا منها؟',
 'ev_close_p': 'أخبرنا بما تريد النظر فيه، وسيرتب الفريق لقاءً في القاهرة أو مكالمة.',
 'menu_label': 'القائمة',
 'table_label': 'المدخلات والتكامل، جدول قابل للتمرير',
}

LANGS = {"en": EN, "ar": AR}
