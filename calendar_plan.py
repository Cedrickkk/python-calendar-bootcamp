import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

CURRICULUM = {
    1: {
        "title": "Week 1: Environment, Ecosystem, and Language Quirks",
        "days": {
            0: { 
                "morning": ("Python Installation & Tooling", "Ditch basic pip. Set up uv and Poetry for modern dependency management. Understand pyproject.toml relative to Maven's pom.xml."),
                "evening": ("Python Ecosystem & Virtual Envs", "Learn the mechanics of virtual environments (venv), interpreter path isolation, and global vs. local Python runtimes.")
            },
            1: {
                "morning": ("Variables, Expressions, and Dynamic Typing", "Contrast Python's dynamic duck typing with Java’s static type compilation. Explore references and object identity (id(), is vs ==)."),
                "evening": ("Data Types & Structuring", "Deep dive into native collections: Lists, Tuples, Sets, and Dictionaries. Focus on time complexities of lookups.")
            },
            2: { 
                "morning": ("Advanced Conditionals & Pattern Matching", "Master Python 3.10+ match-case structural pattern matching, contrasting it directly with Java/TypeScript switch statements."),
                "evening": ("Comprehensions & Pythonic Iteration", "Master List, Dict, and Set comprehensions. Transition from traditional for loops to expressive, high-performance generation patterns.")
            },
            3: { 
                "morning": ("Functions, Arguments, and Scope", "Understand positional-only arguments, keyword-only (*), *args, and **kwargs. Study LEGB (Local, Enclosing, Global, Built-in) scope."),
                "evening": ("First-Class Functions & Closures", "Write functions that return functions. Map your functional knowledge from TypeScript/Java Streams to lambdas and high-order Python functions.")
            },
            4: { 
                "morning": ("Built-in Functions & Overview", "Review essential built-ins used for data cleaning: zip(), enumerate(), any(), all(), map(), and filter()."),
                "evening": ("Weekend Project Preparation & Review", "Consolidation of Week 1 syntactical mechanics. Fix tooling configurations and prepare for your first mini-build.")
            },
            5: { 
                "project": ("CLI Configuration Parser & Sanitizer", "Build a command-line script utilizing Poetry that parses dirty environments, structures runtime args via match-case, and extracts API clean-keys using dict comprehensions.")
            }
        }
    },
    2: {
        "title": "Week 2: Object-Oriented Python & Modern Type Hinting",
        "days": {
            0: {
                "morning": ("Classes & Instantiation Quirks", "Study __new__ versus __init__. Understand self conceptually compared to Java's implicit this."),
                "evening": ("Class Attributes vs Instance Attributes", "Deep dive into scope differences, namespace dicts (__dict__), and classmethods vs staticmethods.")
            },
            1: {
                "morning": ("Dunder Methods (Magic Methods)", "Implement custom object behavior using operator overloading: __str__, __repr__, __eq__, and __len__."),
                "evening": ("Inheritance & The Diamond Problem", "Explore multiple inheritance, Method Resolution Order (MRO), and the behavior of super().")
            },
            2: {
                "morning": ("Encapsulation & Properties", "Pythonic data protection. Avoid explicit getters/setters; implement @property, setters, and deleters."),
                "evening": ("Abstract Base Classes & Interfaces", "Use the abc module to build runtime and design-time structural interfaces, mapping perfectly to Java interface contracts.")
            },
            3: {
                "morning": ("Comprehensive Type Hinting (Mypy)", "Learn typing primitives (List, Dict, Union, Optional, Any) and configure static type-checking workflows using Mypy."),
                "evening": ("Pydantic V2 for Data Validation", "Master Pydantic BaseModel for validation, schema enforcement, and JSON serialization. Crucial skill for LLM structured outputs.")
            },
            4: {
                "morning": ("Advanced Exceptions & Control Flow", "Trace exception hierarchies. Implement customized Exception classes and catch groups."),
                "evening": ("Structural Review & Architecture", "Compare Spring Boot domain classes with Pydantic schemas to align data mapping mental models.")
            },
            5: {
                "project": ("Structured LLM Schema Simulator", "Build a tool using Pydantic models and ABCs that mimics receiving arbitrary JSON payloads from an AI API, maps them to type-hinted classes, and flags mismatched validation parameters.")
            }
        }
    },
    3: {
        "title": "Week 3: Functional Extensions, File Handling, & IO",
        "days": {
            0: {
                "morning": ("Iterators & The Iterator Protocol", "Demystify __iter__ and __next__. Learn how Python loops underneath the hood."),
                "evening": ("Generators & Memory Optimization", "Build lazy evaluation pipelines using yield and generator expressions. Compare memory consumption when handling large chunks of text.")
            },
            1: {
                "morning": ("Context Managers (with statement)", "Learn resource allocation safety using __enter__ and __exit__. Contrast with Java try-with-resources."),
                "evening": ("Custom Context Managers", "Write custom context utilities using both class-based dunders and the @contextmanager decorator hook.")
            },
            2: {
                "morning": ("Advanced File IO (Pathlib)", "Stop using os.path. Adopt object-oriented file paths using pathlib.Path for cross-platform file system orchestration."),
                "evening": ("Parsing Structured Data (JSON, CSV, YAML)", "Handle multi-format data streams. Read, clean, manipulate, and export unstructured files into validated internal structures.")
            },
            3: {
                "morning": ("Decorators Deep Dive (No-Arg)", "Learn metaprogramming by wrapping functions. Understand closure states and execution ordering."),
                "evening": ("Advanced Parameterized Decorators", "Build complex decorators accepting runtime args (e.g., building custom logging or rate-limiting decorators for API endpoints).")
            },
            4: {
                "morning": ("Regular Expressions (re Module)", "Master string splitting, regex groupings, and metadata extraction patterns necessary for text chunking."),
                "evening": ("Data Slicing Workshop", "Review generator pipelines combined with regular expressions to cleanly tokenize stream data.")
            },
            5: {
                "project": ("Raw Text Document Chunking Engine", "Write a script that processes massive directories of text logs/books using generators, tokenizes them based on regex rules, strips noise via decorators, and stream-writes the output to clean JSON blocks.")
            }
        }
    },
    4: {
        "title": "Week 4: Concurrent, Asynchronous, and Network Programming",
        "days": {
            0: {
                "morning": ("The Python GIL Demystified", "Understand the Global Interpreter Lock, thread-safety, and why CPU-bound Python multi-threading behaves differently than Java."),
                "evening": ("Multi-threading vs Multi-processing", "Implement parallel workloads using concurrent.futures. Know exactly when to deploy ThreadPoolExecutor vs ProcessPoolExecutor.")
            },
            1: {
                "morning": ("Intro to Asyncio (Event Loop)", "Understand the single-threaded asynchronous runtime. Contrast co-routines with traditional OS threads."),
                "evening": ("Async/Await Syntax & Control Flow", "Master async def, await, asyncio.gather(), and managing task lifecycles under stress.")
            },
            2: {
                "morning": ("Network Requests with HTTPX", "Transition away from requests. Master httpx for both synchronous and modern native asynchronous HTTP calls."),
                "evening": ("Concurrent API Scraping Protocols", "Build a high-performance network client that dispatches dozens of simultaneous web fetches efficiently without blocking execution.")
            },
            3: {
                "morning": ("Advanced Async Data Streams", "Study async generators (async for) and context managers (async with). Learn how streaming tokens from an LLM works on the wire."),
                "evening": ("Handling Flaky Networks & Backoff", "Implement advanced error catching, rate-limit resolution, and retry loops inside highly concurrent async workers.")
            },
            4: {
                "morning": ("Logging & Diagnostic Tracing", "Configure production-ready loggers using the logging module to parse async execution graphs without cross-contamination."),
                "evening": ("Performance Profiling Basics", "Use cProfile and time blocks to identify latency bottlenecks across async networks.")
            },
            5: {
                "project": ("Concurrent LLM Evaluation Engine Simulator", "Spin up an asynchronous network harness using httpx and asyncio that hitting simulated target mock APIs concurrently, processes results in parallel processing queues, and profiles the roundtrip times.")
            }
        }
    },
    5: {
        "title": "Week 5: Testing, Package Distribution, & Backend APIs",
        "days": {
            0: {
                "morning": ("Modern Testing with Pytest", "Learn the idiomatic pytest framework. Skip verbose assertion methods for clean, standard Python asset operations."),
                "evening": ("Pytest Fixtures & Parametrization", "Leverage reusable context states with @pytest.fixture. Drive matrix data validation using parametrization hooks.")
            },
            1: {
                "morning": ("Mocking & Async Patching", "Mock external integrations using unittest.mock. Test edge cases like network timeouts or broken API objects safely."),
                "evening": ("FastAPI Foundations", "Build microservices using FastAPI. Map your Spring Boot controller concepts directly to FastAPI routers and dynamic route paths.")
            },
            2: {
                "morning": ("FastAPI Dependency Injection", "Master the Depends() architecture. Contrast its local execution graph cleanly with Spring's heavy runtime IoC container."),
                "evening": ("Middleware, State, and Security Hooks", "Implement custom request filtering, trace handlers, and API-key security injection verification layers inside backend systems.")
            },
            3: {
                "morning": ("Packaging Code with Build Artifacts", "Understand wheels (.whl), source distributions (sdist), and package configurations inside modern pyproject.toml specs."),
                "evening": ("CI/CD Pipelines & Linting/Formatting", "Automate your static code checks. Implement ruff for hyper-fast linting/formatting alongside static checking hooks in GitHub actions.")
            },
            4: {
                "morning": ("Dockerizing Python Services", "Construct optimized multi-stage Docker builds. Manage Python dependency sizes, caching layers, and security privileges."),
                "evening": ("Architecture Validation", "End-to-end integration mapping from router interface down to mocked testing models.")
            },
            5: {
                "project": ("Secured FastAPI Microservice Container", "Build an production-grade FastAPI microservice that parses validation schemas via Pydantic, passes automated fixture-driven unit testing grids, and runs inside a minimized Docker container environment.")
            }
        }
    },
    6: {
        "title": "Week 6: Applied AI Application Infrastructure Foundations",
        "days": {
            0: {
                "morning": ("Vector Primitives & Numpy Introduction", "Learn vector representations and linear matrices conceptually using arrays. Learn how dot product operations calculate cosine similarity scores."),
                "evening": ("Working with Vector Databases (Chroma/FAISS)", "Use native Python database client drivers to instantiate memory-mapped index storages, insert mock data arrays, and search via query logic.")
            },
            1: {
                "morning": ("Structured Tokenization Systems", "Use tiktoken or tokenization matrices to inspect string footprints. Look under the hood to see how strings split into integer sequences."),
                "evening": ("Building a Pure-Python RAG Pipeline", "No LangChain. No frameworks. Wire up raw programmatic files, calculate cosine distances natively, extract top nodes, and append to prompt wrappers.")
            },
            2: {
                "morning": ("Function Calling & Tool Definition", "Construct OpenAI/Anthropic spec-compliant JSON schemas using Pydantic models to inform LLMs of local system capabilities."),
                "evening": ("Parsing & Dispatching LLM Tool Actions", "Take incoming LLM tool selection calls, extract parameterized payload variables, route them to clean native functions, and map back execution payloads.")
            },
            3: {
                "morning": ("State Management & Chat History Hooks", "Build robust sliding-window sliding conversation logs to avoid context-window blowouts."),
                "evening": ("Building Deterministic AI Agent Loops", "Program a pure-Python state machine loop executing actions, evaluating terminal output criteria, and trying alternative routes programmatically.")
            },
            4: {
                "morning": ("Streaming API Event Architecture", "Wire up high-speed network chunk streaming pipelines via Server-Sent Events (SSE) out of server nodes down to external subscribers."),
                "evening": ("Capstone Project Architecture Design", "Layout the system diagrams, endpoint pathways, testing configurations, and deployment strategies for your final capstone product.")
            },
            5: {
                "project": ("Capstone Implementation Day 1", "Begin crafting the 'Intelligent Context Broker'. Set up the async text ingestion parser and localized vector lookup schemas.")
            },
            6: { 
                "project": ("Capstone Implementation Day 2 & System Verification", "Finish the agent execution loops, hook up real-time SSE token stream routes, and verify endpoint matrices under pytest mock engines.")
            }
        }
    }
}

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def get_or_create_bootcamp_calendar(service, name="Python AI Bootcamp"):
    try:
        calendar_list = service.calendarList().list().execute()
        for calendar in calendar_list.get('items', []):
            if calendar['summary'] == name:
                print(f"Found existing calendar: '{name}'")
                return calendar['id']
        
        print(f"Creating a fresh target calendar: '{name}'")
        calendar_meta = {'summary': name, 'timeZone': 'Asia/Manila'}
        created_calendar = service.calendars().insert(body=calendar_meta).execute()
        return created_calendar['id']
    except HttpError as error:
        print(f"An error occurred: {error}")
        return 'primary'

def build_event_body(title, description, start_dt, end_dt):
    return {
        'summary': title,
        'description': description,
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Manila'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Manila'},
        'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}]}
    }

def populate_calendar():
    service = get_calendar_service()
    calendar_id = get_or_create_bootcamp_calendar(service)
    
    start_date = datetime.date(2026, 7, 6)
    
    print("Beginning event parsing and scheduling injection pipeline...")
    
    for week_num, week_data in CURRICULUM.items():
        week_offset = (week_num - 1) * 7
        current_week_start = start_date + datetime.timedelta(days=week_offset)
        
        for day_offset, sessions in week_data['days'].items():
            session_date = current_week_start + datetime.timedelta(days=day_offset)
            
            if "morning" in sessions:
                m_title, m_desc = sessions["morning"]
                s_time = datetime.datetime.combine(session_date, datetime.time(6, 0))
                e_time = datetime.datetime.combine(session_date, datetime.time(7, 0))
                event = build_event_body(f"[AM] {m_title}", m_desc, s_time, e_time)
                service.events().insert(calendarId=calendar_id, body=event).execute()
                
            if "evening" in sessions:
                e_title, e_desc = sessions["evening"]
                s_time = datetime.datetime.combine(session_date, datetime.time(19, 0))
                e_time = datetime.datetime.combine(session_date, datetime.time(21, 0))
                event = build_event_body(f"[PM] {e_title}", e_desc, s_time, e_time)
                service.events().insert(calendarId=calendar_id, body=event).execute()
                
            if "project" in sessions:
                p_title, p_desc = sessions["project"]
                s_time = datetime.datetime.combine(session_date, datetime.time(13, 0))
                e_time = datetime.datetime.combine(session_date, datetime.time(17, 0))
                event = build_event_body(f"[PROJECT] {p_title}", p_desc, s_time, e_time)
                service.events().insert(calendarId=calendar_id, body=event).execute()
                
        print(f"Successfully synchronized execution logs for: {week_data['title']}")

    print("\nInitialization Complete. All 6 weeks of metrics are populated in your Google Calendar.")

if __name__ == '__main__':
    populate_calendar()