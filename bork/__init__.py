from .apt_reqs import AptReq, AptUpgrade
from .git_reqs import GitRepoReq
from .os_reqs import FileReq, TemplatedFileReq, LinkedFileReq, FileExistsReq, FileDoesNotExistReq, CommandReq
from .pip_reqs import PipReq
from .service_reqs import ServiceReq
from .base_req import Requirement