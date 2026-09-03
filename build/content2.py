# -*- coding: utf-8 -*-
"""Built Industry, Use Cases, Company and Discuss Your Needs."""

# ---------------------------------------------------------------- BUILT INDUSTRY
BUILT = dict(
    title="Built Industry | TwoSuns",
    desc="The organizations, institutions, materials, services and operating activities that create, supply, "
         "finance, construct, own, transact, maintain and renew built assets.",
    eyebrow="Built Industry",
    h1="One connected industry around the complete life of built assets.",
    sub="The built industry includes the organizations, institutions, materials, services and operating activities "
        "that create, supply, finance, construct, own, transact, maintain and renew built assets.",
    primary=("Explore Built-Industry Use Cases", "use-cases.html"),
    secondary="Discuss Your Industry Context",

    areas_h="Six connected operating areas",
    areas=[
        ("Materials and Manufacturing",
         "The organizations that develop and produce the materials, equipment, systems and fixtures incorporated "
         "into built assets.",
         ["Raw and processed materials",
          "Building products and assemblies",
          "Equipment, machinery and controls",
          "Fixtures, finishes and specialized systems",
          "Industrial and off-site manufacturing"]),
        ("Distribution and Logistics",
         "The commercial and physical networks that move products, materials and equipment to the places where "
         "they are sold, installed and used.",
         ["Wholesale and distribution",
          "Retail and dealer networks",
          "Warehousing and inventory",
          "Transportation and logistics",
          "Supply-chain and fulfilment services"]),
        ("Asset Owners and Investors",
         "The private, public and institutional organizations that fund, commission, own and oversee built assets.",
         ["Private developers and owners",
          "Governments and public agencies",
          "Institutional and infrastructure investors",
          "Corporate and industrial asset owners",
          "Community and not-for-profit owners"]),
        ("Construction and Professional Services",
         "The constructors, specialists and advisers that plan, design, approve and deliver built assets.",
         ["General contractors and trade contractors",
          "Architects, engineers and technical consultants",
          "Project, cost and construction managers",
          "Surveying, testing and inspection services",
          "Specialist, legal, financial and advisory services"]),
        ("Asset Transactions and Operations",
         "The organizations and services that commercialize, occupy, operate, maintain and renew completed assets.",
         ["Sales, brokerage and transactions",
          "Rental, leasing and occupancy",
          "Property, facility and portfolio management",
          "Maintenance, repair and reliability",
          "Renovation, retrofit, reuse and decommissioning"]),
        ("Industry Institutions and Enablement",
         "The organizations that establish requirements, develop capability and represent the interests of "
         "participants across the industry.",
         ["Regulators and authorities",
          "Standards, certification and compliance bodies",
          "Industry, professional and member associations",
          "Education, training and research institutions",
          "Labour, advocacy and public-policy organizations"]),
    ],

    life_h="The built-asset lifecycle connects them",
    life_p="A built asset moves through planning, investment, design, supply, construction, transaction, use, "
           "operation, maintenance, renewal and eventual reuse or retirement. Each stage creates relationships, "
           "requirements and information that affect the stages around it.",
    life_stages=["Planning", "Investment", "Design", "Supply", "Construction", "Transaction",
                 "Use", "Operation", "Maintenance", "Renewal", "Reuse or retirement"],

    cond_h="Conditions shared across the industry",
    cond=[
        "Long asset, product and project lifecycles",
        "Many organizations contributing to one outcome",
        "Regional requirements and operating practices",
        "Complex commercial, technical and regulatory relationships",
        "Physical, financial, market and operational inputs",
        "Frequent handoffs across organizational boundaries",
        "Continuing value after construction is complete",
    ],

    flow_h="Follow the workflow across the ecosystem",
    flow_p="A growth opportunity identified by a manufacturer may influence distribution, specification, "
           "procurement, construction and asset operation. An operating issue identified by an owner may create "
           "requirements for consultants, contractors, suppliers, regulators and service providers. The built "
           "industry is connected through these continuing workflows.",
    close_primary="Explore Built-Industry Use Cases",
    close_secondary="Discuss Your Industry Context",
)

# ---------------------------------------------------------------- USE CASES
UC_THEMES = [
    "Strategy, planning and enterprise performance",
    "Markets, revenue and ecosystem intelligence",
    "Campaigns, events and stakeholder engagement",
    "Products, programs and projects",
    "Operations, supply chain and assets",
    "Governance, compliance and organizational coordination",
]

# (theme index, title, users, inputs, workflow, outputs, lens)
UC_ITEMS = [
    (0, "Executive planning and performance visibility",
     "Executives, finance leaders, business-unit leaders and operators",
     "Financial, operational, commercial, market and organizational inputs",
     "Define the executive view, connect supporting inputs, establish measures and organize recurring review activity.",
     "A coherent enterprise view with visible supporting context, priorities, performance and follow-through.",
     "Core, Ray, Horizon and Pulse"),
    (0, "Investment, resource and initiative prioritization",
     "Executives, finance, portfolio leaders and functional leadership",
     "Strategic objectives, initiatives, budgets, resources, market context, dependencies and expected value",
     "Compare initiatives, test assumptions, assess constraints and maintain the approved priority framework as conditions change.",
     "A transparent allocation framework, prioritized roadmap and continuing visibility into implementation.",
     "Horizon with Pulse execution"),
    (1, "Regional market expansion",
     "Executives, strategy, growth and business-development teams",
     "Market activity, geography, segments, competitors, customer types, projects and organizational capacity",
     "Model addressable markets, compare regions and segments, identify priority opportunities and connect them to growth activity.",
     "Focused market priorities, opportunity maps, growth plans and executive visibility.",
     "Horizon"),
    (1, "Commercial ecosystem and relationship analysis",
     "Growth, partnership, investor-relations and stakeholder teams",
     "Organizations, investors, partners, owners, consultants, contractors, relationships, activity and external research",
     "Build the ecosystem, classify participants, map relationships and influence, monitor developments and coordinate engagement.",
     "A living ecosystem view that supports partner, investor, account and stakeholder development.",
     "Horizon"),
    (1, "Accounts, opportunities, tenders and proposals",
     "Sales, business development, estimating, commercial and leadership teams",
     "Accounts, relationships, opportunity information, tender documents, requirements, pricing and prior submissions",
     "Qualify the opportunity, coordinate contributors, compare requirements, develop the response and maintain follow-through.",
     "Stronger pursuit coordination, reusable knowledge, visible status and commercial continuity.",
     "Horizon with Pulse delivery inputs"),
    (2, "Integrated campaign planning and execution",
     "Marketing, growth, sales, communications and subject experts",
     "Objectives, audiences, market context, content, channels, calendar, activity and response",
     "Develop the campaign plan, coordinate content and approvals, manage execution and connect engagement with commercial follow-up.",
     "Aligned campaigns, faster content coordination and clearer connection between activity and growth.",
     "Horizon"),
    (2, "Events, members and stakeholder programs",
     "Associations, member organizations, public affairs, partnerships and event teams",
     "Stakeholder records, member context, event plans, speakers, content, communications, participation and follow-up",
     "Plan the program, coordinate contributors, manage engagement and preserve the relationship history for continuing activity.",
     "More coherent programs, stronger follow-up and lasting stakeholder context.",
     "Horizon"),
    (3, "Product and research portfolio coordination",
     "Product, research, engineering, commercialization and executive teams",
     "Programs, products, experiments, applications, resources, milestones, market context and partnerships",
     "Structure the portfolio, connect related work, coordinate milestones and resources, and maintain visibility across scientific, technical and commercial activity.",
     "Clearer portfolio priorities, stronger cross-functional coordination and preserved knowledge.",
     "Pulse with Horizon commercialization context"),
    (3, "Estimating, quantity take-offs and materials",
     "Estimators, commercial teams, project leaders, procurement and technical specialists",
     "Drawings, specifications, historical estimates, quantities, rates, materials, supplier inputs and scope revisions",
     "Extract and validate quantities, develop the estimate, compare revisions, prepare materials requirements and coordinate commercial review.",
     "Faster estimate development, visible assumptions, reusable benchmarks and stronger handover into delivery.",
     "Pulse"),
    (3, "Project planning, resources and progress",
     "Project executives, project managers, superintendents, planners, trades and owners",
     "Scope, schedule, milestones, resources, equipment, procurement, dependencies, constraints, progress and documents",
     "Connect the plan, coordinate resources and dependencies, monitor progress and maintain shared project visibility.",
     "Earlier constraint awareness, stronger coordination and a continuing record of project activity.",
     "Pulse"),
    (4, "Procurement, inventory and supplier coordination",
     "Procurement, supply chain, finance, project and operations teams",
     "Suppliers, purchase commitments, materials, inventory movements, delivery dates, costs and operating requirements",
     "Coordinate requirements, compare suppliers, track commitments and inventory, and connect supply activity with projects and operations.",
     "Improved material visibility, supplier coordination, working-capital context and delivery readiness.",
     "Pulse"),
    (4, "Manufacturing economics and production performance",
     "Executives, finance, production, procurement, inventory and commercial teams",
     "Orders, production, recipes, materials, inventory, procurement, expenses, capacity and operating inputs",
     "Connect agreed source domains, define calculation and allocation structures, monitor performance and support recurring executive review.",
     "Traceable production economics, clearer cost and margin context, and stronger operational coordination.",
     "Pulse with Horizon commercial context"),
    (4, "Asset operations, maintenance and reliability",
     "Asset owners, facility teams, maintenance, operations, finance and service providers",
     "Asset records, work history, inspections, operating readings, machine inputs, service requirements, costs and documents",
     "Organize asset context, prioritize work, coordinate maintenance and service activity, and maintain performance history.",
     "Improved reliability, coordinated work, stronger lifecycle knowledge and clearer asset-performance visibility.",
     "Pulse"),
    (5, "Regulatory, quality and compliance workflows",
     "Compliance, quality, legal, technical, operations and leadership teams",
     "Requirements, standards, policies, evidence, inspections, findings, responsibilities and actions",
     "Connect obligations to workflows, coordinate evidence and reviews, track follow-through and preserve the supporting record.",
     "More consistent compliance activity, visible accountability and accessible evidence.",
     "Pulse with Core governance"),
    (5, "Document intelligence and organizational knowledge",
     "Technical, project, commercial, operational and knowledge-management teams",
     "Documents, specifications, contracts, procedures, reports, correspondence, revisions and human expertise",
     "Ingest and classify material, extract relevant content, compare versions, connect information to active work and capture lessons learned.",
     "Faster access to relevant knowledge, stronger continuity and reduced recreation of prior work.",
     "Core, Ray, Horizon and Pulse"),
]

USECASES = dict(
    title="Use Cases | TwoSuns",
    desc="Representative enterprise workflows that combine Horizon and Pulse capabilities across the built industry.",
    eyebrow="Representative Use Cases",
    h1="Configure TwoSuns around the work your organization needs to advance.",
    sub="TwoSuns combines capabilities from Horizon and Pulse around practical enterprise workflows. The examples "
        "below show representative applications. Additional workflows can be modelled as new needs and "
        "opportunities emerge across the built industry.",
    primary="Discuss This Use Case",
    secondary="Tell Us About a Different Workflow",
    close_h="Bring us the workflow",
    close_p=[
        "Every organization combines people, inputs, systems and operating practices differently. TwoSuns can be "
        "configured around a use case already described here or another workflow that matters to your organization.",
        "Selected use cases can be supported by short product demonstrations, detailed walkthroughs, presentations "
        "and training material where available.",
    ],
    close_primary="Discuss This Use Case",
    close_secondary="Tell Us About a Different Workflow",
)

# ---------------------------------------------------------------- COMPANY
COMPANY = dict(
    title="Company | TwoSuns",
    desc="Enterprise strategy, product leadership, industry knowledge, growth expertise, analytics, software "
         "engineering, artificial intelligence, data engineering and implementation capability.",
    eyebrow="Company",
    h1="Enterprise experience applied to the next generation of work.",
    sub="TwoSuns brings together enterprise strategy, product leadership, industry knowledge, growth expertise, "
        "analytics, software engineering, artificial intelligence, data engineering and implementation capability.",
    primary="Discuss Your Needs",
    purpose_h="Our purpose",
    purpose=[
        "We build practical enterprise capability that helps organizations grow, operate and coordinate complex "
        "work through connected context, intelligence and configurable workflows.",
        "Our team works directly with clients to understand the operating environment, configure the platform, "
        "connect the required inputs and develop capabilities that can expand with the organization.",
    ],
    groups=[
        ("Leadership", True, [
            ("Aiman El-Ramly", "Chief Executive Officer",
             "Aiman leads TwoSuns strategy, client engagement and enterprise development, bringing more than 30 "
             "years of experience serving clients across technology, heavy industry, construction, real estate and "
             "the broader built-industry landscape."),
            ("Ryan Arian", "Chief Digital Product Officer",
             "Ryan leads product strategy, platform architecture and the continuing development of TwoSuns, "
             "connecting enterprise requirements with scalable product, integration and implementation capability."),
            ("Ahmed Ghazey", "Director, Engineering and Delivery",
             "Ahmed leads engineering delivery and coordinates the technical work required to configure, extend "
             "and implement TwoSuns for enterprise use."),
        ]),
        ("Product, analytics and engineering", False, [
            ("Sara ElElimy", "Director, Analytics",
             "Sara leads analytics and business discovery, translating enterprise priorities, workflows and inputs "
             "into structured platform requirements and outputs."),
            ("Bhupat Patel", "Senior Full-Stack Engineer",
             "Bhupat develops enterprise application capabilities, interfaces and integrations across the TwoSuns platform."),
            ("Omar Ezzar", "Product Engineer",
             "Omar supports product engineering, configuration and the implementation of platform experiences "
             "around client requirements."),
            ("Yuva Raja", "Senior AI Engineer",
             "Yuva leads applied intelligence and agentic capabilities that operate within the context, controls "
             "and workflows configured in TwoSuns."),
            ("Mohamed Nasser", "AI Engineer",
             "Mohamed develops and supports context-aware intelligence, workflow assistance and related platform capabilities."),
            ("Rakesh Bommavaram", "Data Engineering",
             "Rakesh develops the input pipelines, models and information structures that connect enterprise "
             "sources with the TwoSuns environment."),
            ("AbdelAziz", "Data Engineer",
             "AbdelAziz supports input integration, transformation and the reliable movement of enterprise "
             "information through the platform."),
            ("AbdelRahmen", "Systems Engineer",
             "AbdelRahmen supports the systems, environments and technical operations required for dependable "
             "platform delivery."),
        ]),
        ("Growth and engagement", False, [
            ("Michelle Mollineaux", "Marketing Director",
             "Michelle leads marketing direction, communications and market-facing programs that build awareness "
             "and engagement around TwoSuns."),
            ("Nour Eldin", "AI Solution Advisor",
             "Nour supports business development, client relationships and the coordination of opportunities from "
             "initial interest through active engagement."),
            ("Raihaan Mohammad", "Digital Assets",
             "Raihaan develops and coordinates digital assets that support product communication, demonstrations "
             "and market engagement."),
            ("Alexa Marquez", "Marketing Coordinator",
             "Alexa supports campaign, content and marketing coordination across TwoSuns growth activities."),
            ("Mariam Ibrahim", "Marketing Coordinator",
             "Mariam supports marketing programs, communications and the continuing coordination of campaign activity."),
        ]),
    ],
    aepg_h="TwoSuns by AEPG",
    aepg_p="TwoSuns is developed by AEPG, an enterprise technology and growth organization that brings together "
           "strategy, product, engineering, analytics and implementation expertise.",
    close_primary="Discuss Your Needs",
)

# ---------------------------------------------------------------- DISCUSS
DISCUSS = dict(
    title="Discuss Your Needs | TwoSuns",
    desc="Share the pain point, opportunity or workflow that matters to your organization.",
    eyebrow="Start a Conversation",
    h1="Tell us what you are trying to advance.",
    sub="Share the pain point, opportunity or workflow that matters to your organization. We will review the "
        "context and follow up with a focused conversation about the most useful next step.",
    areas=["Platform", "Horizon", "Pulse", "Built Industry workflow", "Implementation", "General enquiry"],
    confirm_h="Thank you.",
    confirm_p="We have received your message and will review the context before following up.",
    support_h="Contextual supporting material",
    support_p="Product demonstrations, articles, presentations, technical material and training resources appear "
              "beside the page content they support. A central Resources page can be introduced when the available "
              "library provides sufficient depth.",
    support=[
        "Platform demonstrations and architecture material on Platform",
        "Capability walkthroughs within the relevant Horizon or Pulse group",
        "Workflow demonstrations and examples within Use Cases",
        "Team articles beside relevant industry or capability content",
        "Training and enablement material within implementation-related content",
    ],
)

# ---------------------------------------------------------------- CROSS LINKS AND FILTERS
# The document asks Use Cases to filter by built-industry area and user group, and each
# capability group to link through to related use cases. It does not specify the mapping,
# so the assignments below are proposed and easy to change.

UC_AREA_LABELS = ["Materials and Manufacturing", "Distribution and Logistics",
                  "Asset Owners and Investors", "Construction and Professional Services",
                  "Asset Transactions and Operations", "Industry Institutions and Enablement"]

UC_GROUP_LABELS = ["Executive and finance", "Growth and commercial", "Marketing and communications",
                   "Product and engineering", "Project and delivery", "Operations and supply chain",
                   "Asset and facility", "Compliance and quality"]

# use case title -> (built-industry area indices, user group indices)
UC_TAGS = {
    "Executive planning and performance visibility":       ([0, 1, 2, 3, 4, 5], [0]),
    "Investment, resource and initiative prioritization":  ([2, 0, 3], [0]),
    "Regional market expansion":                           ([0, 1], [1]),
    "Commercial ecosystem and relationship analysis":      ([2, 5], [1]),
    "Accounts, opportunities, tenders and proposals":      ([3, 0], [1, 4]),
    "Integrated campaign planning and execution":          ([0, 1], [2]),
    "Events, members and stakeholder programs":            ([5], [2]),
    "Product and research portfolio coordination":         ([0], [3]),
    "Estimating, quantity take-offs and materials":        ([3, 0], [4]),
    "Project planning, resources and progress":            ([3, 2], [4]),
    "Procurement, inventory and supplier coordination":    ([1, 0], [5]),
    "Manufacturing economics and production performance":  ([0], [5, 0]),
    "Asset operations, maintenance and reliability":       ([4, 2], [6]),
    "Regulatory, quality and compliance workflows":        ([5, 3], [7]),
    "Document intelligence and organizational knowledge":  ([0, 1, 2, 3, 4, 5], [7, 3]),
}

# capability group title -> related use case titles
CAP_LINKS = {
    "Market and competitive intelligence": [
        "Regional market expansion", "Commercial ecosystem and relationship analysis"],
    "Growth strategy and market expansion": [
        "Regional market expansion", "Investment, resource and initiative prioritization"],
    "Accounts, opportunities, tenders and proposals": [
        "Accounts, opportunities, tenders and proposals", "Estimating, quantity take-offs and materials"],
    "Campaigns, communications, events and stakeholders": [
        "Integrated campaign planning and execution", "Events, members and stakeholder programs"],
    "Partnerships, investors, channels and relationships": [
        "Commercial ecosystem and relationship analysis", "Events, members and stakeholder programs"],
    "Revenue coordination and commercial performance": [
        "Executive planning and performance visibility", "Accounts, opportunities, tenders and proposals"],
    "Products, portfolios, programs and projects": [
        "Product and research portfolio coordination", "Project planning, resources and progress"],
    "Estimating, costing and commercial delivery": [
        "Estimating, quantity take-offs and materials", "Accounts, opportunities, tenders and proposals"],
    "Planning, scheduling and resource coordination": [
        "Project planning, resources and progress", "Estimating, quantity take-offs and materials"],
    "Procurement, materials, inventory and supply chain": [
        "Procurement, inventory and supplier coordination",
        "Manufacturing economics and production performance"],
    "Manufacturing, operations, assets and maintenance": [
        "Manufacturing economics and production performance",
        "Asset operations, maintenance and reliability"],
    "Workflows, documents, quality, compliance and performance": [
        "Regulatory, quality and compliance workflows",
        "Document intelligence and organizational knowledge"],
}


# Events, from Michelle's "Events for the website" document. Dates carry an ISO
# end date so the page can retire an event once it has finished, and so the list
# can be sorted without parsing prose.
EVENTS = dict(
    title="Events | TwoSuns",
    desc="Meet the TwoSuns team at industry events across the built industry, technology and "
         "building materials sectors.",
    eyebrow="Events",
    h1="Meet the TwoSuns team.",
    sub="We attend and speak at events across the built industry, building materials and "
        "enterprise technology. If you will be at one of these, we would welcome the conversation.",
    primary="Discuss Your Needs",
    secondary="Arrange a Meeting",
    items=[
        dict(name="Egypt Projects 2026",
             ends="2026-09-07",
             dates="5 to 7 September 2026",
             venue="Egypt International Exhibition Center, Cairo, Egypt",
             heading="Meet TwoSuns.ai at Egypt Projects 2026",
             body="TwoSuns.ai will be attending Egypt Projects 2026, the 9th International "
                  "Exhibition for Construction and Building Materials. The event brings together "
                  "leading exhibitors, industry professionals, and government representatives "
                  "from across the construction sector.",
             link="Learn more about Egypt Projects 2026", url="https://www.egypt-projects.com/"),
        dict(name="INTERCEM 2026",
             ends="2026-09-10",
             dates="8 to 10 September 2026",
             venue="Swissotel The Bosphorus, Istanbul, Turkiye",
             heading="Meet TwoSuns.ai at INTERCEM 2026",
             body="TwoSuns.ai will be attending INTERCEM 2026 in Istanbul, where our Founder and "
                  "Chief Executive Officer, Aiman El-Ramly, will be speaking.",
             link="Learn more about INTERCEM 2026", url="https://www.intercemevents.com/event/intercem2026/summary"),
        dict(name="Techne Summit Cairo 2026",
             ends="2026-09-27",
             dates="26 to 27 September 2026",
             venue="Ghurnata Community Space, Cairo, Egypt",
             heading="Meet TwoSuns.ai at Techne Summit Cairo 2026",
             body="TwoSuns.ai will be attending Techne Summit Cairo, a flagship gathering where "
                  "innovation meets capital and policy. The event brings together decision-makers, "
                  "corporations, investors, and global technology leaders to build partnerships and "
                  "help shape the future of emerging markets.",
             link="Learn more about Techne Summit Cairo", url="https://www.technesummit.com/2026"),
        dict(name="Egypt Mining Forum 2026",
             ends="2026-09-29",
             dates="28 to 29 September 2026",
             venue="The St. Regis New Capital, Cairo, Egypt",
             heading="Meet TwoSuns.ai at Egypt Mining Forum 2026",
             body="TwoSuns.ai will be attending the Egypt Mining Forum 2026, a leading platform "
                  "bringing together government, industry, investors, and technology leaders to "
                  "help shape the future of mining in Egypt and beyond.",
             link="Learn more about Egypt Mining Forum 2026", url="https://www.egyptminingforum.com/"),
        dict(name="SaaS North 2026",
             ends="2026-11-05",
             dates="4 to 5 November 2026",
             venue="Ottawa, Ontario, Canada",
             heading="Meet TwoSuns.ai at SaaS North 2026",
             body="TwoSuns.ai is heading to SaaS North 2026 in Ottawa. Hear from Ryan Arian, "
                  "Chief Digital Product Officer, during his speaking session and visit our booth "
                  "to meet the team.",
             link="Learn more about SaaS North 2026", url="https://www.saasnorth.com/"),
        dict(name="AICCE29",
             ends="2026-11-25",
             dates="23 to 25 November 2026",
             venue="Heliopolis Congress Complex, Waldorf Astoria and Hilton Heliopolis Hotels, Cairo, Egypt",
             heading="Meet TwoSuns.ai at AICCE29",
             body="TwoSuns.ai will speak and exhibit at the 29th Arab International Cement and "
                  "Building Materials Conference and Exhibition (AICCE29) in Cairo. Hear from our "
                  "Founder and Chief Executive Officer, Aiman El-Ramly, during his speaking "
                  "session and visit our booth to meet the team.",
             link="Learn more about AICCE29", url="https://www.aucbm.net/welcome"),
        dict(name="LEAP 2026",
             ends="2026-09-03",
             dates="31 August to 3 September 2026",
             venue="RECC Malham, Riyadh, Saudi Arabia",
             heading="Meet TwoSuns.ai at LEAP 2026",
             body="TwoSuns.ai will be attending LEAP 2026, where the global technology community "
                  "gathers in Riyadh to connect, collaborate, and explore what is next.",
             link="Visit the LEAP 2026 website", url="https://onegiantleap.com/"),
    ],
    close_h="Not attending one of these?",
    close_p="Tell us what you are trying to advance and we will arrange a conversation, at an "
            "event or on a call.",
    close_primary="Discuss Your Needs",
    close_secondary="Arrange a Meeting",
)
